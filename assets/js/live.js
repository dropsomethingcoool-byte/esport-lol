/* esport-lol.com — live.js
   Recharge /live.json toutes les 60s et rend :
   #live-countdown : compte à rebours vers le prochain match
   #live-matches   : liste des matchs (direct + à venir)
   #live-results   : matchs terminés (résultats)
   Aucune donnée inventée : si absent, on affiche « — ».
*/
(function () {
  var LIVE_URL = "/live.json";
  var POLL_MS = 60000;
  var state = null;

  function esc(s) {
    return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }

  function fmtTime(iso) {
    if (!iso) return "";
    var d = new Date(iso);
    try {
      return new Intl.DateTimeFormat("fr-FR", {
        weekday: "short", day: "numeric", month: "short",
        hour: "2-digit", minute: "2-digit", timeZone: "Europe/Paris"
      }).format(d);
    } catch (e) { return iso; }
  }

  function allMatches() {
    var out = [];
    if (state) state.stages.forEach(function (st) { st.matches.forEach(function (m) { out.push(m); }); });
    return out;
  }

  function isReal(m) {
    return m.teams.some(function (t) { return t.code && t.code !== "TBD"; });
  }

  function badge(m) {
    if (m.state === "inProgress") return '<span class="badge badge-live">En direct</span>';
    if (m.state === "completed") return '<span class="badge badge-soon">Terminé</span>';
    return '<span class="badge badge-soon">À venir</span>';
  }

  function score(m) {
    if (m.state === "unstarted") return '<span class="vs">VS</span>';
    var a = m.teams[0], b = m.teams[1];
    return '<span class="score">' + (a.gameWins) + ' – ' + (b.gameWins) + '</span>';
  }

  function crest(t, cls) {
    // Logo de l'équipe si dispo (réécrit http:// -> https:// pour éviter le mixed content),
    // sinon retombe sur le code texte (déjà le cas avant).
    var u = t && t.image;
    if (u) {
      u = String(u).replace(/^http:\/\//i, "https://");
      return '<img class="' + cls + '" src="' + esc(u) + '" alt="' + esc(t.code || "") + '" loading="lazy" referrerpolicy="no-referrer">';
    }
    return '<span class="' + cls + '">' + esc(t.code || "?") + '</span>';
  }

  function matchCard(m) {
    var a = m.teams[0], b = m.teams[1];
    return '<div class="match-card">' +
      '<div class="match-meta">' + badge(m) + '<span class="match-time">' + esc(fmtTime(m.startTime)) + '</span></div>' +
      '<div class="match-row">' +
        '<div class="team">' + crest(a, "team-crest") + '<span class="team-name">' + esc(a.name || "") + '</span></div>' +
        '<div class="match-vs">' + score(m) + '</div>' +
        '<div class="team team-right"><span class="team-name">' + esc(b.name || "") + '</span>' + crest(b, "team-crest") + '</div>' +
      '</div></div>';
  }

  function renderCountdown() {
    var el = document.getElementById("live-countdown");
    if (!el) return;
    var next = state && state.next_match;
    if (!next || !next.startTime) { el.textContent = "Planning à venir"; return; }
    var t = new Date(next.startTime).getTime() - Date.now();
    if (t <= 0) {
      el.textContent = next.state === "inProgress" ? "En direct" : "Match imminent";
      return;
    }
    var d = Math.floor(t / 86400000);
    var h = Math.floor((t % 86400000) / 3600000);
    var m = Math.floor((t % 3600000) / 60000);
    var s = Math.floor((t % 60000) / 1000);
    var parts = [];
    if (d > 0) parts.push(d + "j");
    parts.push((h < 10 ? "0" : "") + h + ":" + (m < 10 ? "0" : "") + m + ":" + (s < 10 ? "0" : "") + s);
    el.textContent = parts.join(" ");
  }

  function renderMatches() {
    var el = document.getElementById("live-matches");
    if (!el) return;
    var order = { inProgress: 0, unstarted: 1, completed: 2 };
    var ms = allMatches().filter(isReal).sort(function (a, b) {
      return (order[a.state] || 9) - (order[b.state] || 9);
    });
    el.innerHTML = ms.slice(0, 6).map(matchCard).join("") || '<p class="muted">Aucun match programmé.</p>';
  }

  function renderResults() {
    var el = document.getElementById("live-results");
    if (!el) return;
    var done = (state.results && state.results.length)
      ? state.results
      : allMatches().filter(isReal).filter(function (m) { return m.state === "completed"; });
    if (!done.length) { el.innerHTML = '<p class="muted">Aucun résultat pour le moment.</p>'; return; }
    el.innerHTML = done.map(matchCard).join("");
  }

  function standingsGroup(st) {
    var rows = st.teams.map(function (t, i) {
      var w = t.wins == null ? "–" : t.wins;
      var l = t.losses == null ? "–" : t.losses;
      var bilan = (w === "–" || l === "–") ? "–" : (w + "-" + l);
      var elim = t.eliminated ? ' <span class="s-elim">éliminé</span>' : '';
      return '<tr>' +
        '<td class="s-rank">' + (i + 1) + '</td>' +
        '<td class="s-team">' + crest(t, "s-crest") + '<span class="s-name">' + esc(t.name || "") + elim + '</span></td>' +
        '<td class="s-num">' + w + '</td>' +
        '<td class="s-num">' + l + '</td>' +
        '<td class="s-num s-bilan">' + bilan + '</td>' +
        '</tr>';
    }).join("");
    return '<div class="standings-group">' +
      '<h3 class="standings-title">' + esc(st.title || st.stage_name || "Classement") + '</h3>' +
      '<table class="standings-table"><thead><tr>' +
      '<th class="s-rank">#</th><th class="s-team">Équipe</th>' +
      '<th class="s-num">V</th><th class="s-num">D</th><th class="s-num">Bilan</th>' +
      '</tr></thead><tbody>' + rows + '</tbody></table></div>';
  }

  function renderStandings() {
    var el = document.getElementById("live-standings");
    if (!el) return;
    var sts = state && state.standings;
    if (!sts || !sts.length) {
      el.innerHTML = '<p class="muted">Le classement sera disponible dès les premiers résultats des Worlds 2026.</p>';
      return;
    }
    el.innerHTML = sts.map(standingsGroup).join("");
  }

  function render() {
    renderCountdown();
    renderMatches();
    renderResults();
    renderStandings();
    updateOtpBanner();
  }

  function load() {
    fetch(LIVE_URL, { cache: "no-store" })
      .then(function (r) { return r.json(); })
      .then(function (d) { state = d; render(); })
      .catch(function () { /* silencieux : on garde le dernier état */ });
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", load);
  else load();
  setInterval(load, POLL_MS);
  setInterval(renderCountdown, 1000); // tick du compte à rebours

  // Bandeau « En direct » (site-wide) : affiché uniquement si un match est en cours
  function updateOtpBanner() {
    var banner = document.getElementById("otp-banner");
    if (!banner) return;
    var liveMatch = null;
    if (state) {
      var ms = allMatches().filter(isReal).filter(function (m) {
        return m.state === "inProgress";
      });
      liveMatch = ms[0] || null;
    }
    var sub = document.getElementById("otp-banner-sub");
    var cta = document.getElementById("otp-banner-cta");
    if (liveMatch) {
      banner.hidden = false;
      var a = liveMatch.teams[0], b = liveMatch.teams[1];
      var aw = a.gameWins != null ? a.gameWins : 0;
      var bw = b.gameWins != null ? b.gameWins : 0;
      if (sub) sub.textContent = "En direct : " + (a.code || "?") + " " + aw + " – " + bw + " " + (b.code || "?");
      if (cta) { cta.textContent = "▶ Regarder en direct"; cta.href = "/"; }
    } else {
      banner.hidden = true;
    }
  }

  // Bandeau cliquable : déplie un lecteur Twitch OTP en dessous du header
  var otpBanner = document.getElementById("otp-banner");
  var otpPlayer = document.getElementById("otp-player");
  if (otpBanner && otpPlayer) {
    var otpLoaded = false;
    function toggleOtpPlayer() {
      if (!otpLoaded) {
        otpPlayer.querySelector(".otp-player-inner").innerHTML =
          '<iframe src="https://player.twitch.tv/?channel=otplol_&parent=esport-lol.com&parent=www.esport-lol.com" ' +
          'width="100%" height="360" allow="autoplay; fullscreen" allowfullscreen></iframe>';
        otpLoaded = true;
      }
      var hidden = otpPlayer.hidden;
      otpPlayer.hidden = !hidden;
      otpBanner.setAttribute("aria-expanded", hidden ? "true" : "false");
    }
    otpBanner.addEventListener("click", toggleOtpPlayer);
    otpBanner.addEventListener("keydown", function (e) {
      if (e.key === "Enter" || e.key === " ") { e.preventDefault(); toggleOtpPlayer(); }
    });
  }

  // Embed Twitch (chaîne OTP LoL), chargé au clic pour ne pas ralentir la page
  var twBtn = document.getElementById("twitch-load");
  if (twBtn) {
    twBtn.addEventListener("click", function () {
      var host = document.getElementById("twitch-player");
      host.innerHTML = '<iframe src="https://player.twitch.tv/?channel=otplol_&parent=esport-lol.com&parent=www.esport-lol.com" width="100%" height="360" allow="autoplay; fullscreen" allowfullscreen></iframe>';
      twBtn.style.display = "none";
    });
  }
})();
