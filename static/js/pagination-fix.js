/**
 * pagination-fix.js - Script pour assurer que la pagination reste sur une ligne
 * Ce script vérifie que la pagination ne déborde pas et permet le défilement si nécessaire
 */

document.addEventListener('DOMContentLoaded', function() {
  // Fonction pour assurer que la pagination reste sur une ligne
  function ensureSingleLinePagination() {
    const paginationContainer = document.querySelector('.pagination-container');
    
    if (!paginationContainer) return;
    
    // Sur tous les écrans
    // Centrer la page courante si on n'est pas proche du début ou de la fin
    const currentPage = paginationContainer.querySelector('.current');
    if (currentPage) {
      // Ajouter un délai pour permettre au rendu de s'effectuer
      setTimeout(function() {
        // Calculer la position pour centrer la page courante
        const containerWidth = paginationContainer.offsetWidth;
        const linkWidth = currentPage.offsetWidth;
        const linkPosition = currentPage.offsetLeft;
        
        // Effectuer un défilement doux vers la page courante
        if (linkPosition > containerWidth / 2) {
          const scrollPosition = Math.max(0, linkPosition - containerWidth / 2 + linkWidth / 2);
          paginationContainer.scrollLeft = scrollPosition;
        }
      }, 100);
    }
  }
  
  // Exécuter au chargement
  ensureSingleLinePagination();
  
  // Réexécuter en cas de redimensionnement
  window.addEventListener('resize', ensureSingleLinePagination);
});
