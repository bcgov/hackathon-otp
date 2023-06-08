const express = require("express");
const request = require("request");

const defaultConfig = {
  everifyHost: "localhost:8000",
  routePrefix: "/everify",
};

function getMiddleware(configuration) {
  const config = configuration || defaultConfig;

  // Internal router to forward to the API
  const internalRouter = express.Router();

  // Handle submit form endpoint with OTP
  internalRouter.post("/verify", (req, res, next) => {
    console.log("Verify!");
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
    if (!req.claims) next();

    const isVerifiedUrl = new URL(`${config.everifyHost}/is_verified`);
    isVerifiedUrl.searchParams.append(
      "email_address",
      req.claims.email_address
    );
    isVerifiedUrl.searchParams.append("auth_provider_uuid", req.claims.uuid);

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
      body: {
        email_address: req.claims.email_address,
        auth_provider_uuid: req.claims.uuid,
      },
    });
    if (!sendEmailResponse.ok)
      throw new Error("error calling send email endpoint");

    // Show the user the OTP page
    const verifyPageUrl = new URL(`${config.everifyHost}/is_verified`);
    verifyPageUrl.searchParams.append("route_prefix", config.route_prefix);
    verifyPageUrl.searchParams.append(
      "email_address",
      req.claims.email_address
    );
    verifyPageUrl.searchParams.append("auth_provider_uuid", req.claims.uuid);

    request({
      url: verifyPageUrl,
    }).pipe(res);
  });

  return router;
}

module.exports = { getMiddleware, defaultConfig };

/// consumer would do
// app.use(package.getMiddleware( {..optional config..} ))
