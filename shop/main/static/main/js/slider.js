const swiper = new Swiper(".swiper", {
  loop: true, // безкінечний цикл
  autoplay: {
    delay: 3000, // авто‑зміна кожні 3 секунди
    disableOnInteraction: false,
  },
  pagination: {
    el: ".swiper-pagination",
    clickable: true,
  },
  navigation: {
    nextEl: ".swiper-button-next",
    prevEl: ".swiper-button-prev",
  },
});
