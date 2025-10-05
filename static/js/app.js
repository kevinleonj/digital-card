// app.js
(function () {
  // Copy email to clipboard when clicking the email button
  var mailLink = document.getElementById("lnk_email");
  if (mailLink) {
    mailLink.addEventListener("click", function () {
      try {
        var email = mailLink.getAttribute("href").replace("mailto:", "");
        if (navigator && navigator.clipboard && email) {
          navigator.clipboard.writeText(email).catch(function () {});
        }
      } catch (e) {}
    });
  }
  // Hide avatar if load fails
  var avatar = document.querySelector(".avatar");
  if (avatar) {
    avatar.addEventListener("error", function () {
      try { avatar.style.display = "none"; } catch (e) {}
    });
  }
})();
