const express = require("express");
const request = require("request");

const config = {
  everify_host: "...",
  route_prefix: "everify",
};

const getMiddleware = (config) => {
  const router = express.Router();

  // Handle submit form endpoint with OTP
  router.use("/verify", (req, res, next) => {});

  // Handle static assets for verify page
  router.use("/static/:filename", (req, res) => {
    request({
      uri: `${everify_host}/static/${req.params.filename}`,
    }).pipe(res);
  });

  router.use(async (req, res, next) => {
    const isVerifiedUrl = new URL(`${everify_host}/is_verified`);
    isVerifiedUrl.searchParams.append(
      "email_address",
      req.claims.email_address
    );
    isVerifiedUrl.searchParams.append("auth_provider_uuid", req.claims.uuid);

    const isVerifiedResponse = await fetch(isVerifiedUrl);

    if (isVerifiedResponse.ok) {
      next();
    }

    // Send email
    const sendEmailUrl = new URL(`${everify_host}/create_otp`);
    const sendEmailResponse = await fetch(sendEmailUrl, {
      method: "POST",
      body: {
        email_address: req.claims.email_address,
        auth_provider_uuid: req.claims.uuid,
      },
    });
    if (!sendEmailResponse.ok) throw "error calling send email endpoint";

    // Show the user the OTP page
    const verifyPageUrl = new URL(`${everify_host}/is_verified`);
    verifyPageUrl.searchParams.append("route_prefix", "everify");
    verifyPageUrl.searchParams.append(
      "email_address",
      req.claims.email_address
    );
    verifyPageUrl.searchParams.append("auth_provider_uuid", req.claims.uuid);

    request({
      url: verifyPageUrl,
    }).pipe(res);
  });
};

/// consumer would do
// app.use('/everify', getMiddleware())
