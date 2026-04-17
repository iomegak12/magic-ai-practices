/**
 * API Drift Verification Test Script
 * ====================================
 * Purpose : Prove the correct backend paths (from backend-openapi.json)
 *           vs the wrong paths (from PM API Specification).
 *
 * Run     : node api-drift-test.js
 * Requires: Node.js 18+ (uses native fetch)
 *
 * Author  : Ramkumar
 * Date    : 2026-02-20
 */

const BASE_URL = "http://localhost:9080";

// ─────────────────────────────────────────────────────────────────────────────
// Colour helpers (works without any npm packages)
// ─────────────────────────────────────────────────────────────────────────────
const c = {
  reset:  "\x1b[0m",
  green:  "\x1b[32m",
  red:    "\x1b[31m",
  yellow: "\x1b[33m",
  cyan:   "\x1b[36m",
  bold:   "\x1b[1m",
  dim:    "\x1b[2m",
};

const pass  = `${c.green}${c.bold}  PASS${c.reset}`;
const fail  = `${c.red}${c.bold}  FAIL${c.reset}`;
const wrong = `${c.yellow}${c.bold}  404 (as expected — wrong path)${c.reset}`;

// ─────────────────────────────────────────────────────────────────────────────
// Test counters
// ─────────────────────────────────────────────────────────────────────────────
let totalTests    = 0;
let passedTests   = 0;
let failedTests   = 0;
let sessionId     = null;   // Created during test — reused across tests

// ─────────────────────────────────────────────────────────────────────────────
// Core helpers
// ─────────────────────────────────────────────────────────────────────────────
async function request(method, path, body = null) {
  const options = {
    method,
    headers: { "Content-Type": "application/json", Accept: "application/json" },
  };
  if (body) options.body = JSON.stringify(body);

  try {
    const res = await fetch(`${BASE_URL}${path}`, options);
    let data = null;
    try { data = await res.json(); } catch (_) { /* non-JSON body */ }
    return { status: res.status, data };
  } catch (err) {
    return { status: 0, error: err.message };
  }
}

function printHeader(title) {
  console.log(`\n${c.cyan}${c.bold}${"═".repeat(65)}${c.reset}`);
  console.log(`${c.cyan}${c.bold}  ${title}${c.reset}`);
  console.log(`${c.cyan}${"═".repeat(65)}${c.reset}`);
}

function printRow(label, result) {
  totalTests++;
  const statusText = result.ok
    ? `${pass}  [HTTP ${result.status}]`
    : result.expectedWrong
    ? `${wrong}  [HTTP ${result.status}]`
    : `${fail}  [HTTP ${result.status}]`;

  if (result.ok) passedTests++;
  else if (!result.expectedWrong) failedTests++;

  console.log(`  ${c.bold}${label.padEnd(38)}${c.reset} ${statusText}`);
  if (result.ok && result.note) {
    console.log(`  ${c.dim}  ↳ ${result.note}${c.reset}`);
  }
  if (!result.ok && !result.expectedWrong && result.reason) {
    console.log(`  ${c.red}  ↳ Error: ${result.reason}${c.reset}`);
  }
}

// ─────────────────────────────────────────────────────────────────────────────
// Individual test runners
// ─────────────────────────────────────────────────────────────────────────────

// ── 1. Health Endpoints ──────────────────────────────────────────────────────
async function testHealthEndpoints() {
  printHeader("1 · HEALTH ENDPOINTS");

  // Basic health — same in both spec & backend
  const health = await request("GET", "/health");
  printRow("GET /health", {
    ok:     health.status === 200,
    status: health.status,
    note:   health.data ? `status="${health.data.status}"` : "",
  });

  // ── Readiness ──
  console.log(`\n  ${c.yellow}Readiness Check${c.reset}`);

  const readyCorrect = await request("GET", "/health/ready");
  printRow("GET /health/ready  ✔ CORRECT", {
    ok:     readyCorrect.status === 200,
    status: readyCorrect.status,
    note:   readyCorrect.data ? `ready=${readyCorrect.data.ready}` : "",
  });

  const readyWrong = await request("GET", "/health/readiness");
  printRow("GET /health/readiness  ✘ PM SPEC", {
    ok:            false,
    expectedWrong: readyWrong.status === 404 || readyWrong.status === 0,
    status:        readyWrong.status,
  });

  // ── Liveness ──
  console.log(`\n  ${c.yellow}Liveness Check${c.reset}`);

  const liveCorrect = await request("GET", "/health/live");
  printRow("GET /health/live  ✔ CORRECT", {
    ok:     liveCorrect.status === 200,
    status: liveCorrect.status,
  });

  const liveWrong = await request("GET", "/health/liveness");
  printRow("GET /health/liveness  ✘ PM SPEC", {
    ok:            false,
    expectedWrong: liveWrong.status === 404 || liveWrong.status === 0,
    status:        liveWrong.status,
  });
}

// ── 2. Agent — Create Session ────────────────────────────────────────────────
async function testCreateSession() {
  printHeader("2 · CREATE SESSION");

  // ── Correct path ──
  const correctRes = await request("POST", "/agent/sessions", {
    session_id: `test-session-${Date.now()}`,
    metadata:   { user_name: "Ramkumar", channel: "web" },
  });

  const created = correctRes.status === 201;
  if (created) sessionId = correctRes.data?.session_id;

  printRow("POST /agent/sessions  ✔ CORRECT", {
    ok:     created,
    status: correctRes.status,
    note:   sessionId ? `session_id="${sessionId}"` : "",
    reason: !created ? JSON.stringify(correctRes.data) : "",
  });

  // ── Wrong path (PM spec) ──
  const wrongRes = await request("POST", "/api/v1/agent/sessions", {
    session_id: `test-wrong-${Date.now()}`,
  });

  printRow("POST /api/v1/agent/sessions  ✘ PM SPEC", {
    ok:            false,
    expectedWrong: wrongRes.status === 404 || wrongRes.status === 0,
    status:        wrongRes.status,
  });
}

// ── 3. Agent — List Sessions ─────────────────────────────────────────────────
async function testListSessions() {
  printHeader("3 · LIST SESSIONS");

  const correctRes = await request("GET", "/agent/sessions");
  printRow("GET /agent/sessions  ✔ CORRECT", {
    ok:     correctRes.status === 200,
    status: correctRes.status,
    note:   correctRes.data ? `total_count=${correctRes.data.total_count}` : "",
  });

  const wrongRes = await request("GET", "/api/v1/agent/sessions");
  printRow("GET /api/v1/agent/sessions  ✘ PM SPEC", {
    ok:            false,
    expectedWrong: wrongRes.status === 404 || wrongRes.status === 0,
    status:        wrongRes.status,
  });
}

// ── 4. Agent — Send Message ──────────────────────────────────────────────────
async function testSendMessage() {
  printHeader("4 · SEND MESSAGE");

  if (!sessionId) {
    console.log(`  ${c.yellow}⚠ Skipping — no session_id available (Create Session may have failed)${c.reset}`);
    return;
  }

  const correctRes = await request("POST", "/agent/messages", {
    session_id: sessionId,
    message:    "Hello, this is a drift verification test message.",
  });

  printRow("POST /agent/messages  ✔ CORRECT", {
    ok:     correctRes.status === 200,
    status: correctRes.status,
    note:   correctRes.data?.response
      ? `agent replied: "${correctRes.data.response.substring(0, 60)}..."`
      : "",
    reason: correctRes.status !== 200 ? JSON.stringify(correctRes.data) : "",
  });

  const wrongRes = await request("POST", "/api/v1/agent/messages", {
    session_id: sessionId,
    message:    "Wrong path test",
  });

  printRow("POST /api/v1/agent/messages  ✘ PM SPEC", {
    ok:            false,
    expectedWrong: wrongRes.status === 404 || wrongRes.status === 0,
    status:        wrongRes.status,
  });
}

// ── 5. Agent — Delete Session ────────────────────────────────────────────────
async function testDeleteSession() {
  printHeader("5 · DELETE SESSION");

  if (!sessionId) {
    console.log(`  ${c.yellow}⚠ Skipping — no session_id available${c.reset}`);
    return;
  }

  // Test wrong path first (session still exists)
  const wrongRes = await request("DELETE", `/api/v1/agent/sessions/${sessionId}`);
  printRow(`DELETE /api/v1/agent/sessions/{id}  ✘ PM SPEC`, {
    ok:            false,
    expectedWrong: wrongRes.status === 404 || wrongRes.status === 0,
    status:        wrongRes.status,
  });

  // Now delete using correct path
  const correctRes = await request("DELETE", `/agent/sessions/${sessionId}`);
  printRow(`DELETE /agent/sessions/{id}  ✔ CORRECT`, {
    ok:     correctRes.status === 200,
    status: correctRes.status,
    note:   correctRes.data?.status === "deleted" ? `status="${correctRes.data.status}"` : "",
    reason: correctRes.status !== 200 ? JSON.stringify(correctRes.data) : "",
  });
}

// ── 6. Info Endpoints ────────────────────────────────────────────────────────
async function testInfoEndpoints() {
  printHeader("6 · INFO ENDPOINTS");

  // ── API Info ──
  console.log(`\n  ${c.yellow}API Info${c.reset}`);

  const infoCorrect = await request("GET", "/info");
  printRow("GET /info  ✔ CORRECT", {
    ok:     infoCorrect.status === 200,
    status: infoCorrect.status,
    note:   infoCorrect.data?.version ? `version="${infoCorrect.data.version}"` : "",
    reason: infoCorrect.status !== 200
      ? JSON.stringify(infoCorrect.data ?? infoCorrect.error)
      : "",
  });

  const infoWrong = await request("GET", "/api/v1/info");
  printRow("GET /api/v1/info  ✘ PM SPEC", {
    ok:            false,
    expectedWrong: infoWrong.status === 404 || infoWrong.status === 0,
    status:        infoWrong.status,
  });

  // ── List Tools ──
  console.log(`\n  ${c.yellow}List Tools${c.reset}`);

  const toolsCorrect = await request("GET", "/info/tools");
  printRow("GET /info/tools  ✔ CORRECT", {
    ok:     toolsCorrect.status === 200,
    status: toolsCorrect.status,
    note:   toolsCorrect.data?.total_count !== undefined
      ? `total_count=${toolsCorrect.data.total_count}`
      : "",
  });

  const toolsWrong = await request("GET", "/api/v1/tools");
  printRow("GET /api/v1/tools  ✘ PM SPEC", {
    ok:            false,
    expectedWrong: toolsWrong.status === 404 || toolsWrong.status === 0,
    status:        toolsWrong.status,
  });
}

// ── 7. Session Management (Bonus) ────────────────────────────────────────────
async function testSessionManagement() {
  printHeader("7 · SESSION MANAGEMENT  (these paths match in both specs)");

  const statsRes = await request("GET", "/api/v1/sessions/stats");
  printRow("GET /api/v1/sessions/stats", {
    ok:     statsRes.status === 200,
    status: statsRes.status,
    note:   statsRes.data?.total_sessions !== undefined
      ? `total_sessions=${statsRes.data.total_sessions}`
      : "",
  });

  const listRes = await request("GET", "/api/v1/sessions?limit=5&offset=0");
  printRow("GET /api/v1/sessions", {
    ok:     listRes.status === 200,
    status: listRes.status,
    note:   listRes.data?.total !== undefined
      ? `total=${listRes.data.total}  (field is "total" not "total_count")`
      : "",
  });
}

// ─────────────────────────────────────────────────────────────────────────────
// Summary
// ─────────────────────────────────────────────────────────────────────────────
function printSummary() {
  const driftTests = totalTests - passedTests - failedTests;
  console.log(`\n${c.cyan}${c.bold}${"═".repeat(65)}${c.reset}`);
  console.log(`${c.cyan}${c.bold}  TEST SUMMARY${c.reset}`);
  console.log(`${c.cyan}${"═".repeat(65)}${c.reset}`);
  console.log(`  Total tests run   : ${c.bold}${totalTests}${c.reset}`);
  console.log(`  ${c.green}Correct paths PASS${c.reset} : ${c.bold}${passedTests}${c.reset}`);
  console.log(`  ${c.yellow}Wrong paths = 404 ${c.reset} : ${c.bold}${driftTests}${c.reset}  (drift confirmed)`);
  if (failedTests > 0) {
    console.log(`  ${c.red}Unexpected failures${c.reset}: ${c.bold}${failedTests}${c.reset}  ← investigate!`);
  }
  console.log(`\n  ${c.dim}Base URL tested: ${BASE_URL}${c.reset}`);
  console.log(`${c.cyan}${"═".repeat(65)}${c.reset}\n`);
}

// ─────────────────────────────────────────────────────────────────────────────
// Entry point
// ─────────────────────────────────────────────────────────────────────────────
(async () => {
  console.log(`\n${c.bold}${c.cyan}  API Drift Verification — Customer Service Agent${c.reset}`);
  console.log(`  ${c.dim}Testing: ${BASE_URL}${c.reset}`);
  console.log(`  ${c.dim}Date   : ${new Date().toISOString()}${c.reset}`);

  await testHealthEndpoints();
  await testCreateSession();
  await testListSessions();
  await testSendMessage();
  await testDeleteSession();
  await testInfoEndpoints();
  await testSessionManagement();

  printSummary();
})();
