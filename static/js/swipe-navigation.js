// Script de navigation par swipe pour HitSearch
// Permet de naviguer entre les cartes par swipe sur mobile et desktop

// Variables globales
let currentCardIndex = -1;
let allCards = [];
let startX, startY, startTime;
let touchThreshold = 50; // Distance minimale pour détecter un swipe
let timeThreshold = 300; // Durée maximale pour un swipe (en ms)
let isMobileDevice = false; // Variable pour détecter si on est sur mobile

// Fonction pour détecter si on est sur mobile
function detectMobileDevice() {
  return (window.innerWidth <= 768) || 
         /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
}

// Initialisation au chargement de la page
document.addEventListener('DOMContentLoaded', function() {
  // Récupérer toutes les cartes
  allCards = Array.from(document.querySelectorAll('.carte'));
  
  // Détecter si on est sur mobile
  isMobileDevice = detectMobileDevice();
  
  // Ajouter les flèches de navigation au lightbox (uniquement sur desktop)
  setupLightboxNavigation();
  
  // Ajouter les gestionnaires d'événements pour le swipe sur mobile (touch)
  if (isMobileDevice) {
    setupTouchSwipe();
  }
  
  // Empêcher que le clic sur le contenu du lightbox ferme la modal
  const lightboxContent = document.querySelector('.lightbox-content');
  if (lightboxContent) {
    lightboxContent.addEventListener('click', function(e) {
      e.stopPropagation(); // Empêcher la propagation vers la modal
    });
  }
  
  // Mettre à jour la classe du corps selon le type d'appareil
  document.body.classList.toggle('mobile-device', isMobileDevice);
  
  // Surveiller les changements de taille d'écran
  window.addEventListener('resize', function() {
    const wasMobile = isMobileDevice;
    isMobileDevice = detectMobileDevice();
    
    // Si l'état mobile/desktop a changé
    if (wasMobile !== isMobileDevice) {
      document.body.classList.toggle('mobile-device', isMobileDevice);
      
      // Afficher/masquer les boutons de navigation
      const navButtons = document.querySelectorAll('.lightbox-nav');
      navButtons.forEach(button => {
        button.style.display = isMobileDevice ? 'none' : 'flex';
      });
    }
  });
});

// Configuration des flèches de navigation pour le lightbox
function setupLightboxNavigation() {
  const lightboxContent = document.querySelector('.lightbox-content');
  if (!lightboxContent) return;
  
  // Supprimer les boutons de navigation existants s'ils existent
  const existingNavButtons = lightboxContent.querySelectorAll('.lightbox-nav');
  existingNavButtons.forEach(button => button.remove());
  
  // Créer les boutons de navigation
  const prevButton = document.createElement('button');
  prevButton.className = 'lightbox-nav lightbox-prev';
  prevButton.innerHTML = `
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
      <path d="M15 18l-6-6 6-6"/>
    </svg>
  `;
  prevButton.setAttribute('aria-label', 'Carte précédente');
  
  // Utiliser un gestionnaire d'événements séparé pour prévenir les problèmes de propagation
  const handlePrevClick = function(e) {
    e.stopPropagation();
    e.preventDefault();
    navigateToPrevCard();
    return false;
  };
  
  prevButton.addEventListener('click', handlePrevClick);
  
  const nextButton = document.createElement('button');
  nextButton.className = 'lightbox-nav lightbox-next';
  nextButton.innerHTML = `
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
      <path d="M9 18l6-6-6-6"/>
    </svg>
  `;
  nextButton.setAttribute('aria-label', 'Carte suivante');
  
  // Utiliser un gestionnaire d'événements séparé pour prévenir les problèmes de propagation
  const handleNextClick = function(e) {
    e.stopPropagation();
    e.preventDefault();
    navigateToNextCard();
    return false;
  };
  
  nextButton.addEventListener('click', handleNextClick);
  
  nextButton.addEventListener('click', handleNextClick);
  
  // Masquer les boutons sur mobile
  if (isMobileDevice) {
    prevButton.style.display = 'none';
    nextButton.style.display = 'none';
  }
  
  // Ajouter les boutons au lightbox
  lightboxContent.appendChild(prevButton);
  lightboxContent.appendChild(nextButton);
  
  // Ajouter une petite pause pour s'assurer que les événements sont correctement attachés
  setTimeout(() => {
    console.log("Navigation buttons setup complete");
  }, 100);
}

// Configuration du swipe tactile (mobile)
function setupTouchSwipe() {
  const lightboxModal = document.getElementById('lightbox-modal');
  if (!lightboxModal) return;
  
  lightboxModal.addEventListener('touchstart', handleTouchStart, { passive: true });
  lightboxModal.addEventListener('touchmove', handleTouchMove, { passive: true });
  lightboxModal.addEventListener('touchend', handleTouchEnd, { passive: true });
}

// Gestionnaires d'événements pour le toucher
function handleTouchStart(e) {
  // Ignorer si on touche un bouton ou si on est en train de faire défiler
  if (e.target.closest('button') || e.target.closest('.lightbox-close') || e.target.closest('.lightbox-nav')) return;
  
  const touch = e.touches[0];
  startX = touch.clientX;
  startY = touch.clientY;
  startTime = new Date().getTime();
}

function handleTouchMove(e) {
  if (!startX || !startY) return;
}

function handleTouchEnd(e) {
  if (!startX || !startY) return;
  
  const touch = e.changedTouches[0];
  const endX = touch.clientX;
  const endY = touch.clientY;
  const endTime = new Date().getTime();
  const deltaX = endX - startX;
  const deltaY = endY - startY;
  const elapsedTime = endTime - startTime;
  
  // Vérifier si c'est un swipe (mouvement horizontal plus important que vertical)
  if (elapsedTime < timeThreshold && Math.abs(deltaX) > touchThreshold && Math.abs(deltaX) > Math.abs(deltaY)) {
    if (deltaX > 0) {
      // Swipe vers la droite (carte précédente)
      navigateToPrevCard();
    } else {
      // Swipe vers la gauche (carte suivante)
      navigateToNextCard();
    }
  }
  
  // Réinitialiser les valeurs
  startX = null;
  startY = null;
}

// Fonction pour trouver l'index de la carte actuellement affichée
function findCurrentCardIndex() {
  const lightboxImage = document.getElementById('lightbox-image');
  if (!lightboxImage || !lightboxImage.src) return -1;
  
  return allCards.findIndex(card => {
    const cardImg = card.querySelector('.miniature');
    return cardImg && cardImg.src === lightboxImage.src;
  });
}

// Fonction pour naviguer vers la carte précédente
function navigateToPrevCard() {
  console.log("Navigating to previous card");
  if (allCards.length === 0) return;
  
  if (currentCardIndex === -1) {
    currentCardIndex = findCurrentCardIndex();
    console.log("Current card index:", currentCardIndex);
  }
  
  // Calculer l'index précédent (boucler à la fin si nécessaire)
  const prevIndex = (currentCardIndex > 0) ? currentCardIndex - 1 : allCards.length - 1;
  console.log("Previous index:", prevIndex);
  
  // Afficher la carte précédente
  const prevCard = allCards[prevIndex];
  const prevImg = prevCard.querySelector('.miniature');
  if (prevImg) {
    updateLightbox(prevImg);
    currentCardIndex = prevIndex;
  } else {
    console.error("Could not find image in previous card");
  }
}

// Fonction pour naviguer vers la carte suivante
function navigateToNextCard() {
  console.log("Navigating to next card");
  if (allCards.length === 0) return;
  
  if (currentCardIndex === -1) {
    currentCardIndex = findCurrentCardIndex();
    console.log("Current card index:", currentCardIndex);
  }
  
  // Calculer l'index suivant (boucler au début si nécessaire)
  const nextIndex = (currentCardIndex < allCards.length - 1) ? currentCardIndex + 1 : 0;
  console.log("Next index:", nextIndex);
  
  // Afficher la carte suivante
  const nextCard = allCards[nextIndex];
  const nextImg = nextCard.querySelector('.miniature');
  if (nextImg) {
    updateLightbox(nextImg);
    currentCardIndex = nextIndex;
  }
}

// Fonction pour mettre à jour le lightbox avec une nouvelle image
function updateLightbox(imgElement) {
  if (!imgElement) {
    console.error("Cannot update lightbox: no image element provided");
    return;
  }
  
  const lightboxImage = document.getElementById('lightbox-image');
  const lightboxName = document.getElementById('lightbox-name');
  
  if (!lightboxImage || !lightboxName) {
    console.error("Cannot update lightbox: missing DOM elements");
    return;
  }
  
  console.log("Updating lightbox with image:", imgElement.src);
  
  try {
    // Mise à jour de l'image
    lightboxImage.src = imgElement.src;
    lightboxImage.alt = imgElement.alt || '';
    
    // Mise à jour du nom de la carte
    const cardName = extractCardName(imgElement.src);
    lightboxName.textContent = cardName;
    
    // Ajouter une petite animation de transition
    lightboxImage.classList.add('transitioning');
    setTimeout(() => {
      lightboxImage.classList.remove('transitioning');
    }, 300);
  } catch (error) {
    console.error("Error updating lightbox:", error);
  }
}

// Surcharge de la fonction originale openLightbox pour stocker l'index
const originalOpenLightbox = window.originalOpenLightbox || window.openLightbox;
window.openLightbox = function(imgElement) {
  // Appeler la fonction originale
  originalOpenLightbox(imgElement);
  
  // Mettre à jour l'index de la carte actuelle
  currentCardIndex = findCurrentCardIndex();
  
  // Ajouter des gestionnaires d'événements clavier pour la navigation
  document.addEventListener('keydown', handleKeyNavigation);
};

// Surcharge de la fonction originale closeLightbox pour nettoyer
const originalCloseLightbox = window.originalCloseLightbox || window.closeLightbox;
window.closeLightbox = function() {
  // Appeler la fonction originale
  originalCloseLightbox();
  
  // Réinitialiser l'index
  currentCardIndex = -1;
  
  // Supprimer les gestionnaires d'événements clavier
  document.removeEventListener('keydown', handleKeyNavigation);
};

// Gestion de la navigation par clavier
function handleKeyNavigation(e) {
  if (e.key === 'ArrowLeft') {
    navigateToPrevCard();
    e.preventDefault();
  } else if (e.key === 'ArrowRight') {
    navigateToNextCard();
    e.preventDefault();
  }
}
