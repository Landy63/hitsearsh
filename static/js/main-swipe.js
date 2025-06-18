// Ce fichier contient les fonctions nécessaires pour la navigation par swipe
// Il est chargé après main.js et expose les fonctions nécessaires pour swipe-navigation.js

// On s'assure que les fonctions principales sont correctement exposées dans l'objet window
document.addEventListener('DOMContentLoaded', function() {
  // Stocker les références aux fonctions originales
  if (typeof openLightbox === 'function') {
    window.originalOpenLightbox = openLightbox;
  }
  
  if (typeof closeLightbox === 'function') {
    window.originalCloseLightbox = closeLightbox;
  }
  
  if (typeof extractCardName === 'function') {
    window.originalExtractCardName = extractCardName;
  }
  
  // Détecter si on est sur mobile
  const isMobileDevice = (window.innerWidth <= 768) || 
        /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
  
  // Ajouter la classe mobile-device au body si nécessaire
  document.body.classList.toggle('mobile-device', isMobileDevice);
  
  // Corriger la gestion de clics sur le modal
  const lightboxModal = document.getElementById('lightbox-modal');
  if (lightboxModal) {
    // Supprimer tous les gestionnaires d'événements existants de clic
    const newClickHandler = function(e) {
      // Fermer uniquement si on clique directement sur le fond (pas sur les boutons ou le contenu)
      if (e.target === lightboxModal) {
        closeLightbox();
      }
    };
    
    // S'assurer que nous n'avons qu'un seul gestionnaire d'événements
    lightboxModal.removeEventListener('click', newClickHandler);
    lightboxModal.addEventListener('click', newClickHandler);
    
    // Stockez cette référence pour pouvoir la nettoyer plus tard si nécessaire
    lightboxModal._newClickHandler = newClickHandler;
  }
  
  // Afficher l'indicateur de swipe quand une carte est ouverte (sur mobile uniquement)
  const originalOpenLightboxFn = window.originalOpenLightbox || openLightbox;
  window.openLightbox = function(imgElement) {
    // Appeler la fonction originale
    originalOpenLightboxFn(imgElement);
    
    // Afficher l'indicateur de swipe uniquement sur mobile
    if (isMobileDevice) {
      const swipeIndicator = document.querySelector('.swipe-indicator');
      if (swipeIndicator) {
        swipeIndicator.classList.add('visible');
        setTimeout(() => {
          swipeIndicator.classList.remove('visible');
        }, 3000);
      }
    }
  };
});
