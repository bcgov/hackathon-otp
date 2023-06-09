const express = require("express");
const request = require("request");

const defaultConfig = {
  everifyHost: "http://localhost:8000",
  routePrefix: "/everify",
};

const host = process.env.HOST || "http://localhost:3004";

function getMiddleware(configuration) {
  const config = configuration || defaultConfig;

  // Internal router to forward to the API
  const internalRouter = express.Router();

  // Handle submit form endpoint with OTP
  internalRouter.post("/verify", async (req, res, next) => {
    console.log(req.body);

    const verifyUrl = new URL(`${config.everifyHost}/verify`);

    const data = new URLSearchParams();
    data.append("one_time_password", "3625");
    data.append("email_address", "pbastia@gmail.com");
    data.append(
      "auth_provider_uuid",
      "fd2e5c94f4da4c1393a6e03093e25a85@bceidboth"
    );
    data.append("redirect_url", host);

    const response = await fetch(verifyUrl, {
      method: "POST",
      body: data,
    });

    console.log(response.status);

    if (response.ok) return res.redirect(host);

    // Show the user the OTP page
    const verifyPageUrl = new URL(`${config.everifyHost}/verify_page`);
    verifyPageUrl.searchParams.append("route_prefix", config.routePrefix);
    verifyPageUrl.searchParams.append("email_address", req.claims.email);
    verifyPageUrl.searchParams.append("auth_provider_uuid", req.claims.sub);
    verifyPageUrl.searchParams.append("validation_failed", "true");

    //const verifyPageResponse = await fetch(verifyPageUrl);
    request({
      uri: verifyPageUrl,
    }).pipe(res);
  });

  // Handle static assets for verify page
  internalRouter.get("/static/:filename", (req, res) => {
    request({
      uri: `${config.everifyHost}/static/${req.params.filename}`,
    }).pipe(res);
  });

  // Main middleware
  const router = express.Router();
  router.use(config.routePrefix, internalRouter);

  router.use(async (req, res, next) => {
    if (!req.claims) return next();

    const isVerifiedUrl = new URL(`${config.everifyHost}/is_verified`);
    isVerifiedUrl.searchParams.append("email_address", req.claims.email);
    isVerifiedUrl.searchParams.append("auth_provider_uuid", req.claims.sub);

    const isVerifiedResponse = await fetch(isVerifiedUrl);

    if (isVerifiedResponse.ok) {
      return next();
    }

    if (isVerifiedResponse.status !== 401)
      throw new Error("error calling the is_verified endpoint");

    // Send email
    const sendEmailUrl = new URL(`${config.everifyHost}/create_otp`);
    const sendEmailResponse = await fetch(sendEmailUrl, {
      method: "POST",
      body: JSON.stringify({
        email_address: req.claims.email,
        auth_provider_uuid: req.claims.sub,
      }),
      headers: { "Content-Type": "application/json" },
    });
    if (!sendEmailResponse.ok)
      throw new Error(
        "error calling send email endpoint " + sendEmailResponse.error
      );

    // Show the user the OTP page
    const verifyPageUrl = new URL(`${config.everifyHost}/verify_page`);
    verifyPageUrl.searchParams.append("route_prefix", config.routePrefix);
    verifyPageUrl.searchParams.append("email_address", req.claims.email);
    verifyPageUrl.searchParams.append("auth_provider_uuid", req.claims.sub);

    const verifyPageResponse = await fetch(verifyPageUrl);
    // request({
    //   uri: verifyPageUrl,
    // }).pipe(res);
    const html = await verifyPageResponse.text();
    res.send(html);
    res.status(201);
  });

  return router;
}

module.exports = { getMiddleware, defaultConfig };

/// consumer would do
// app.use('/everify', getMiddleware())
