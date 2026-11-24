### Changelog – WebAI to API

#### v0.7.3 – 2026-11-24

##### Fixed
- Added support for extended Google Workspace / multi-account cookies (`OSID`, `__Secure-OSID`, `SID`, `__Secure-1PSIDCC`) ensuring full authorization without Google redirecting to ServiceLogin.
- Added dynamic model resolution mapping generic model names (`gemini-3.0-flash`, `gemini-3.0-pro`, `gemini-3.0-flash-thinking`) to live internal Google model identifiers (`gemini-neon`, `gemini-4-hydrogen`, `gemini-hydrogen-thinking`).

---

#### v0.7.2 – 2026-11-24

##### Fixed
- Fixed Starlette 1.x `TemplateResponse` positional parameter mismatch in `/admin` endpoint (`TypeError: unhashable type: 'dict'`) by passing keyword arguments `request` and `name`.
- Added a 15-second timeout (`asyncio.wait_for`) and timeout exception handling for `GeminiClient.init()` to prevent indefinite deadlock on `asyncio.Lock` during startup when cookies are invalid or expired, allowing the server and admin dashboard to load properly.

---

#### v0.7.1 – 2026-11-07

##### Fixed
- Upgraded `gemini-webapi` to `>=2.1.1` (along with `curl-cffi>=0.16.2` and `orjson>=3.11.9`), resolving Google streaming stalls (`Response stalled (>60s)`) and body parsing errors caused by Google's updated web RPC protocol.
- Updated supported Python requirement in `pyproject.toml` to `>=3.11,<4.0` to match `gemini-webapi>=2.1.1` and container base image.

##### Added
- **Error Diagnostics & Alert Banner**: Dashboard now immediately detects and highlights stream stalls, parse failures, and expired cookies with actionable troubleshooting tips.
- **Recent Issues History**: Added a dedicated section on the dashboard displaying recent errors, affected endpoints, and recommended fixes with a one-click history clear.
- **Test Generation Button**: Added a "Test Generation" button in the admin interface to instantly verify live Gemini streaming and view response latency.

---

#### v0.x.x – Draft

##### Fixed

- Added missing `nodriver` and `platformdirs` dependencies to `pyproject.toml` for `g4f` server compatibility.
- Unified server runner functions to implement a consistent and graceful shutdown mechanism.

---

#### v0.4.0 – 2025-06-27

##### Added

- Displayed a user message explaining how to use the `gpt4free` server.

##### Fixed

- Resolved execution issue on Windows 11.
- Improved error handling with appropriate user-facing messages.

##### Changed

- Updated internal libraries and dependencies.

---

#### v0.3.0 – 2025-06-25

##### Added

- Improved server startup information display, including available services and API endpoints.
- Added a new method using the [gpt4free v0.5.5.5](https://github.com/xtekky/gpt4free) library, which also functions as a fallback.
- Introduced support for switching between models using keyboard shortcuts (keys `1` and `2`) in the terminal.
- WebAI-to-API now uses your browser and cookies **only for Gemini**, resulting in faster performance.
- `gpt4free` integration provides access to multiple providers (ChatGPT, Gemini, Claude, DeepSeek, etc.), ensuring continuous availability of various models.

##### Changed

- Updated internal libraries.
- Upgraded to [Gemini API v1.14.0](https://github.com/HanaokaYuzu/Gemini-API).

##### Fixed

- Ensured compatibility with Windows (tested on Windows 11).
