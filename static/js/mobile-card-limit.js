/**
 * mobile-card-limit.js - Ajuste le nombre de cartes par page sur mobile
 */

document.addEventListener('DOMContentLoaded', function() {
  // Ne s'exécute que sur les appareils mobiles
  if (window.innerWidth <= 768) {
    // Vérifie si l'utilisateur n'a jamais explicitement défini de préférence
    const urlParams = new URLSearchParams(window.location.search);
    const hasUserSetPerPage = urlParams.has('per_page');
    
    // Si l'utilisateur n'a pas défini de préférence et que per_page n'est pas 50
    if (!hasUserSetPerPage && document.querySelector('.per-page-label')) {
      const perPageText = document.querySelector('.per-page-label').textContent;
      const currentPerPage = parseInt(perPageText);
      
      // Si le nombre actuel n'est pas déjà 50, ajuster automatiquement
      if (currentPerPage && currentPerPage !== 50) {
        // Construire la nouvelle URL avec per_page=50
        let newUrl = new URL(window.location.href);
        newUrl.searchParams.set('per_page', '50');
        
        // Redirection silencieuse (sans déclencher une nouvelle entrée d'historique)
        window.location.replace(newUrl.toString());
      }
    }
  }
});
