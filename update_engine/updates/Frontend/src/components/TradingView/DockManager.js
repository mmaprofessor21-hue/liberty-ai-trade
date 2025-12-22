// DO NOT MODIFY THIS FILE OUTSIDE THE RULES IN README_UPDATER.txt
// NO IMPORT OVERRIDES | NO PATH ASSUMPTIONS | ABSOLUTE STRUCTURE COMPLIANCE

export function enableDrag(element) {
  if (!element) return;

  let isDragging = false;
  let startX = 0;
  let startY = 0;

  element.addEventListener("mousedown", (e) => {
    isDragging = true;
    startX = e.clientX - element.offsetLeft;
    startY = e.clientY - element.offsetTop;
  });

  document.addEventListener("mousemove", (e) => {
    if (!isDragging) return;
    element.style.left = e.clientX - startX + "px";
    element.style.top = e.clientY - startY + "px";
  });

  document.addEventListener("mouseup", () => {
    isDragging = false;
  });
}
