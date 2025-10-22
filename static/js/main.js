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
  // Derive auth flag from body data attribute (set in base.html)
  try {
    const authAttr = document.body && document.body.dataset ? document.body.dataset.authenticated : null;
    window.AUTHENTICATED = (authAttr === 'true');
  } catch (_) { /* noop */ }
  const alert = document.querySelector(".alert");
  if(alert) alert.scrollIntoView({behavior:"smooth", block:"start"});

  // Bloquea envío de donación si no hay sesión y muestra alerta para ir a login
  const donationForm = document.getElementById('donation-form');
  if (donationForm && !window.AUTHENTICATED) {
    donationForm.addEventListener('submit', function(e){
      e.preventDefault();
      if (window.Swal) {
        Swal.fire({
          title: 'Debes iniciar sesión',
          text: 'Para donar, primero inicia sesión o regístrate.',
          icon: 'info',
          showCancelButton: true,
          confirmButtonText: 'Ir al ingreso',
          cancelButtonText: 'Cerrar'
        }).then((result)=>{
          if(result.isConfirmed){
            const next = encodeURIComponent('/#donar');
            window.location.href = '/accounts/login/?next=' + next;
          }
        });
      } else {
        // Fallback sin SweetAlert
        const next = encodeURIComponent('/#donar');
        window.location.href = '/accounts/login/?next=' + next;
      }
    });
  }
});
