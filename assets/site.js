// Points the download button at the newest APK of this game, using the public releases API.
// Without JavaScript or when the API is unavailable, the button keeps linking to the releases page.
(function () {
  var btn = document.getElementById("download");
  if (!btn) return;
  var game = btn.getAttribute("data-game");
  var meta = document.getElementById("meta");
  fetch("https://api.github.com/repos/nbeostar/happy-game-releases/releases?per_page=30")
    .then(function (r) { return r.ok ? r.json() : Promise.reject(new Error(r.status)); })
    .then(function (releases) {
      var prefix = game + "-v";
      var rel = releases.filter(function (r) { return !r.draft && !r.prerelease && r.tag_name.indexOf(prefix) === 0; })[0];
      if (!rel) return;
      var apk = (rel.assets || []).filter(function (a) { return /\.apk$/i.test(a.name); })[0];
      if (!apk) return;
      var version = rel.tag_name.slice(prefix.length);
      var mb = Math.round(apk.size / 1048576);
      btn.href = apk.browser_download_url;
      btn.setAttribute("download", apk.name);
      btn.textContent = "Download voor Android (versie " + version + ")";
      if (meta) {
        var d = new Date(rel.published_at);
        meta.textContent = mb + " MB · " + d.toLocaleDateString("nl-NL", { day: "numeric", month: "long", year: "numeric" }) +
          " · gratis · geen advertenties · werkt zonder internet";
      }
    })
    .catch(function () { /* keep the fallback link */ });
})();
