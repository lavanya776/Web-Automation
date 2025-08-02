## Selenium test automation for E-Commerce Website
This repository contains a professional-grade, Python-based Selenium automation framework built to validate and ensure the quality of a modern e-commerce web application. Leveraging the Page Object Model (POM) architecture, this framework encapsulates UI workflows, providing a scalable, reusable, and maintainable test suite ready for regression, smoke, and workflow automation.

## Why Create This Framework?
Quality and reliability are mission-critical in e-commerce, where UX failures directly impact sales, trust, and brand reputation. Manual testing is laborious, repetitive, and error-prone. This automation framework solves these issues by:

Enabling rapid regression testing after every release or code change.

Improving test coverage for complex user journeys (product discovery, filtering, cart, checkout, profile management).

Catching UI bugs and workflow issues automatically, before they reach customers.

Providing repeatable, auditable, and scalable tests for continuous integration and continuous delivery (CI/CD) environments.

How Was This Framework Built?
Python & Selenium WebDriver: For robust browser automation across Chrome and other browsers.

Page Object Model (POM): Each significant page (Home, Product, Cart, Profile, etc.) is represented as a class, encapsulating selectors and business functions. This promotes modularity and simple maintenance.

Central Test Runner: Orchestrates end-to-end user scenarios using shared WebDriver sessions for realistic workflows.

Automatic Screenshot Capture on Failure: On any test failure, screenshots are saved with timestamped filenames in a dedicated /screenshots directory, expediting debugging and reporting.

Explicit Waits and Advanced Element Locators: Ensures reliable interaction with dynamic web content and asynchronous page loads.

Scope of Automated Testing
This framework enables the automation of critical e-commerce functionality, including but not limited to:

Product Browsing & Search: Validation of product listings, details, search, and filtering (price ranges, categories).

Wishlist & Cart Operations: Adding/removing products to wishlist or cart, verifying cart contents, prices, and quantities.

Checkout & Navigation: Simulating end-to-end purchasing workflows and header/footer navigations.

Profile Management: Secure login, profile updating, and sidebar navigation.

Robustness Checks: Confirming page loads, redirects, and error messaging.
