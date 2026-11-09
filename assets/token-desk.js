"use strict";
async function copyText(text, fallback) {
  try {
    await navigator.clipboard.writeText(text);
    return true;
  } catch {
    if (fallback) { fallback.focus(); fallback.select(); }
    return false;
  }
}

function flash(button, label) {
  const original = button.dataset.label || button.textContent;
  button.dataset.label = original;
  button.textContent = label;
  setTimeout(() => { button.textContent = original; }, 1600);
}

document.addEventListener("DOMContentLoaded", () => {
  // One-time token reveal.
  const button = document.getElementById("copy-token");
  const token = document.getElementById("issued-token");
  const result = document.getElementById("copy-result");
  if (button && token) {
    token.addEventListener("focus", () => token.select());
    button.addEventListener("click", async () => {
      const copied = await copyText(token.value, token);
      result.textContent = copied ? "已复制，请交付给对应接收人" : "请手动复制选中的令牌";
    });
  }

  // Plain values such as the MCP endpoint.
  document.querySelectorAll("[data-copy]").forEach((item) => {
    item.addEventListener("click", async () => {
      flash(item, (await copyText(item.dataset.copy)) ? "已复制" : "复制失败");
    });
  });

  // Identity table filter.
  const filter = document.getElementById("identity-filter");
  if (filter) {
    const rows = Array.from(document.querySelectorAll("[data-identity]"));
    const none = document.getElementById("filter-empty");
    filter.addEventListener("input", () => {
      const query = filter.value.trim().toLowerCase();
      let shown = 0;
      rows.forEach((row) => {
        const match = !query || row.dataset.identity.toLowerCase().includes(query);
        row.hidden = !match;
        shown += match;
      });
      if (none) none.hidden = shown > 0;
    });
  }

  // Only one revoke confirmation open at a time.
  const revokes = document.querySelectorAll("details.revoke");
  revokes.forEach((item) => item.addEventListener("toggle", () => {
    if (item.open) {
      revokes.forEach((other) => { if (other !== item) other.open = false; });
      // Opening the inline form can widen the table. Keep the full confirmation
      // in its horizontal scroll area on narrow screens.
      item.querySelector("form").scrollIntoView({ block: "nearest", inline: "nearest" });
    }
  }));

  // Guide: copy buttons on code blocks and current-section highlighting.
  document.querySelectorAll(".doc-content pre").forEach((pre) => {
    const copy = document.createElement("button");
    copy.type = "button";
    copy.className = "copy-code";
    copy.textContent = "复制";
    copy.addEventListener("click", async () => {
      flash(copy, (await copyText(pre.querySelector("code").textContent)) ? "已复制" : "复制失败");
    });
    pre.appendChild(copy);
  });
  const links = new Map(Array.from(document.querySelectorAll(".doc-nav a")).map((a) => [a.hash.slice(1), a]));
  if (links.size && "IntersectionObserver" in window) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        links.forEach((a) => a.classList.remove("active"));
        const link = links.get(entry.target.id);
        if (link) link.classList.add("active");
      });
    }, { rootMargin: "-80px 0px -70% 0px" });
    links.forEach((_, id) => { const target = document.getElementById(id); if (target) observer.observe(target); });
  }
});

window.addEventListener("pagehide", () => {
  const token = document.getElementById("issued-token");
  if (token) token.value = "";
});
window.addEventListener("pageshow", (event) => {
  if (event.persisted && document.getElementById("issued-token")) location.replace("/admin");
});
