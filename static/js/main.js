// JS extrait de index.html, à l’identique
// Premier script : gestion des sous-catégories, sélecteurs, etc.
// ...copier ici tout le JS de <script>...</content>

// Gestion des cases "Tout sélectionner / Tout désélectionner" pour Eras, Series, Decks
function setupSelectAllCheckbox(selectAllId, groupName) {
  const selectAll = document.getElementById(selectAllId);
  if (!selectAll) return;
  const checkboxes = document.querySelectorAll(`input[type='checkbox'][name='${groupName}']`);

  // Quand on clique sur "Tout sélectionner"
  selectAll.addEventListener('change', function() {
    checkboxes.forEach(cb => {
      cb.checked = selectAll.checked;
    });
    document.getElementById('form-filtres').submit();
  });

  // Quand on clique sur une case individuelle
  checkboxes.forEach(cb => {
    cb.addEventListener('change', function() {
      const allChecked = Array.from(checkboxes).every(c => c.checked);
      selectAll.checked = allChecked;
    });
  });

  // Initialiser l'état de la case "Tout sélectionner"
  const allChecked = Array.from(checkboxes).length > 0 && Array.from(checkboxes).every(c => c.checked);
  selectAll.checked = allChecked;
}

document.addEventListener('DOMContentLoaded', function() {
  setupSelectAllCheckbox('select_all_eras', 'era');
  setupSelectAllCheckbox('select_all_series', 'series');
  setupSelectAllCheckbox('select_all_decks', 'deck');
});
