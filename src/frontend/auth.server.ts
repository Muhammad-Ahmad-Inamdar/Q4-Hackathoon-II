// This file is commented out as we're using backend authentication instead
// import { betterAuth } from "better-auth";
// import { jwt } from "better-auth/plugins";

// export const auth = betterAuth({
//   secret: process.env.BETTER_AUTH_SECRET || "any-solid-secret-123",
//   database: {
//     provider: "sqlite",
//     url: "./db.sqlite", // Ensure path is correct
//   },
//   emailAndPassword: {
//     enabled: true, // Yeh lazmi hai login/signup ke liye
//     autoSignIn: true,
//   },
//   plugins: [
//     jwt({
//       expiresIn: "7d" // Set token expiry to 7 days as per requirements
//     })
//   ], // Agar backend ko token bhejna hai
// });