/* Boston Pain Center — Stripe payment links configuration
 * ------------------------------------------------------------------
 * Boston Pain Center holds the Stripe account. Paste each service's
 * Stripe Payment Link below (Stripe Dashboard > Payments > Payment Links).
 *
 *   1. Create a Payment Link per service in the BPC Stripe account.
 *   2. Replace the "" for that service with the full https://buy.stripe.com/... URL.
 *   3. Keep the quotes. Save, commit, deploy.
 *
 * While a service's link is still "" (empty), the booking page will NOT
 * show a dead button — it shows "Online payment activating soon — call to
 * book" instead. No card data ever touches this site: payment happens on
 * Stripe's hosted checkout page.
 */
var BPC_STRIPE_LINKS = {
  consult_new:        "",  // REPLACE WITH BPC STRIPE LINK — New Patient Consultation
  consult_followup:   "",  // REPLACE WITH BPC STRIPE LINK — Follow-up Visit
  telehealth:         "",  // REPLACE WITH BPC STRIPE LINK — Telehealth Consultation
  second_opinion:     "",  // REPLACE WITH BPC STRIPE LINK — Second Opinion Review
  prp_consult:        "",  // REPLACE WITH BPC STRIPE LINK — PRP Consultation
  regenerative_consult:"", // REPLACE WITH BPC STRIPE LINK — Regenerative Medicine Consultation
  ketamine_screening: "",  // REPLACE WITH BPC STRIPE LINK — Ketamine Screening Visit
  crps_eval:          ""   // REPLACE WITH BPC STRIPE LINK — CRPS Evaluation
};
