// Scroll suave para enlaces internos
document.addEventListener("click", (e) => {
  const a = e.target.closest('a[href^="/#"], a[href^="#"]');
  if (!a) return;
  const id = a.getAttribute("href").replace("/", "");
  const el = document.querySelector(id);
  if (el){
    e.preventDefault();
    el.scrollIntoView({ behavior: "smooth", block: "start" });
    history.replaceState(null, "", id);
  }
});

// Helper: auto-cerrar el menú móvil al clickear
document.addEventListener("click", (e)=>{
  const navLink = e.target.closest(".navbar .nav-link, .navbar .btn");
  const nav = document.getElementById("nav");
  if(navLink && nav && nav.classList.contains("show")){
    const bs = bootstrap.Collapse.getOrCreateInstance(nav);
    bs.hide();
  }
});

document.addEventListener("DOMContentLoaded", ()=>{
  const alert = document.querySelector(".alert");
  if(alert) alert.scrollIntoView({behavior:"smooth", block:"start"});
});