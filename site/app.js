// app.js — zero deps, runs on SWA
(function () {
  // ---------- CONFIG: replace placeholders ----------
  const CFG = {
    linkedin: "https://www.linkedin.com/in/kevinleonj",
    whatsappNumber: "+491736283856",              // digits only, with country code
    email: "kevinleonjouvin@|gmail.com",
    cvUrl: "/cv/kevin_leon_cv.pdf", // or CDN URL
    instagram: "https://www.instagram.com/kevinleonj",
    strava: "https://strava.app.link/NBC6jOl7cXb",
    //classpass: "https://classpass.com/members/83201",       // optional
    portfolio: "https://kevinleonjouvin.com",                   // your site
    friendPhoto: "/images/friend.jpg",
    recruiterPhoto: "/images/recruiter.jpg",
    enableJokes: true,                                         // set true to show jokes
  };

  // Optional SFW dad jokes. Edit or add up to ~50.
  const JOKES = [
  "I told my suitcase we weren't going on vacation. Now it's emotionally checked out.",
  "My phone autocorrected 'meeting' to 'meating.' My calendar is very carnivorous.",
  "I bought a ceiling fan. Turns out it's just a huge advocate.",
  "I told my plants I'd water them later. They started a drought protest.",
  "I wanted to be a baker, but I couldn't make enough dough.",
  "I named my Wi‑Fi 'Nacho Wi‑Fi.' People still ask if it's nacho network.",
  "Asked the librarian for books on paranoia. She whispered, 'They're behind you.'",
  "Installed a doorbell that tells jokes. Now every delivery is a stand‑up.",
  "Opened a bakery called 'Kneadful Things.' Business rose instantly.",
  "Claustrophobic people are excellent at social distancing.",
  "Told a joke about a broken pencil. It had no point but drew smiles.",
  "My calendar and I argued. It's still holding a grudge for next Tuesday.",
  "Bought a map of the world. It's been quite a journey so far.",
  "Put my money in an outfit. Now it's a little overdressed.",
  "Invented a new word: Plagiarism.",
  "Told my watch to stop wasting time. It's now in therapy.",
  "The inventor of autocorrect died. Restaurant? Rest in peace.",
  "Told my coffee we were breaking up. I need someone less bitter.",
  "Gave my fridge a password. Now my snacks have better security.",
  "Dad, can you put my shoes on? No, I'll stand.",
  "Went to buy camouflage pants but couldn't find any.",
  "Started a band called '666 Megabytes.' We still need a better format.",
  "Tried to write a novel about wind. It was a breeze then blew away.",
  "My suitcase wanted to travel light. I told it to stop carrying feelings.",
  "Asked the invisible man what he does for fun. He said, 'I'm an open book.'",
  "I told my alarm clock a joke. It didn't laugh but it did snooze.",
  "Told a joke to my GPS. It recalculated my sense of humor.",
  "Bought a ladder to success. Turns out it was a step ladder.",
  "Signed up for a procrastinators club. Meeting postponed indefinitely.",
  "I asked my mirror who's the fairest. It replied, 'Error 404: Humility not found.'"
];


  // ---------- helpers ----------
  const qs = (s) => document.querySelector(s);
  const elLinks = qs("#links");
  const elAvatar = qs("#avatar");
  const chipFriend = qs("#chip-friend");
  const chipRecruiter = qs("#chip-recruiter");
  const mode = (['/r'].includes(location.pathname)) ? 'recruiter' : 'friend';

  function waLink(num) {
    const digits = (num || "").replace(/\D/g, "");
    return digits.length >= 8 ? `https://wa.me/${digits}` : "#";
  }

  function link(label, href, id) {
    const a = document.createElement("a");
    a.id = id;
    a.className = "btn";
    a.role = "button";
    a.tabIndex = 0;
    a.rel = "noopener noreferrer";
    a.target = "_blank";
    a.textContent = label;
    a.href = href || "#";
    return a;
  }

  function renderLinksFriend() {
    const L = [];
    L.push(link("Instagram", CFG.instagram, "lnk_instagram"));
    L.push(link("WhatsApp", waLink(CFG.whatsappNumber), "lnk_whatsapp"));
    L.push(link("LinkedIn", CFG.linkedin, "lnk_linkedin"));
    if (CFG.strava) L.push(link("Strava", CFG.strava, "lnk_strava"));
    if (CFG.portfolio) L.push(link("Portfolio", CFG.portfolio, "lnk_portfolio"));
    return L;
}

  function renderLinksRecruiter() {
    // Order: CV, LinkedIn, Email  (no Instagram, no WhatsApp)
    const L = [];
    L.push(link("CV (PDF)", CFG.cvUrl, "lnk_cv"));
    L.push(link("LinkedIn", CFG.linkedin, "lnk_linkedin"));
    L.push(link("Email", `mailto:${CFG.email}`, "lnk_email"));
    return L;
  }

  function render() {
    // chips state
    if (mode === 'friend') {
      chipFriend.classList.add("chip-hot");
      chipFriend.href = "/f";
      chipRecruiter.href = "/r";
      elAvatar.src = CFG.friendPhoto;
      elLinks.replaceChildren(...renderLinksFriend());
    } else {
      chipRecruiter.classList.add("chip-hot");
      chipFriend.href = "/f";
      chipRecruiter.href = "/r";
      elAvatar.src = CFG.recruiterPhoto;
      elLinks.replaceChildren(...renderLinksRecruiter());
    }

    // optional jokes
    if (CFG.enableJokes && JOKES.length) {
      try {
        const key = "kj_seen_jokes";
        const seen = new Set(JSON.parse(localStorage.getItem(key) || "[]"));
        const choices = JOKES.map((_, i) => i).filter(i => !seen.has(i));
        const pick = choices.length ? choices[Math.floor(Math.random() * choices.length)]
                                    : Math.floor(Math.random() * JOKES.length);
        const nextSeen = Array.from(new Set([...seen, pick])).slice(-64);
        localStorage.setItem(key, JSON.stringify(nextSeen));
        document.getElementById("joke-text").textContent = JOKES[pick];
        document.getElementById("joke-wrap").hidden = false;
      } catch (_) { /* non-blocking */ }
    }

    // email copy helper
    const emailBtn = document.getElementById("lnk_email");
    if (emailBtn) {
      emailBtn.addEventListener("click", () => {
        try {
          const addr = (emailBtn.href || "").replace(/^mailto:/, "");
          navigator.clipboard?.writeText(addr);
        } catch (_) {}
      });
    }

    // image load failure → hide
    elAvatar.addEventListener("error", () => { elAvatar.style.display = "none"; });
    try {
        const o = location.origin.replace(/\/$/, "");
        const f = document.getElementById("url-friend");
        const r = document.getElementById("url-recruiter");
        if (f) f.textContent = o + "/";
        if (r) r.textContent = o + "/r";
    } catch (_) {}
  }

  render();
})();
