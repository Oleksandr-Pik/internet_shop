document.addEventListener("htmx:afterSwap", function (event) {
  if (event.target.id === "cart-count") {
    const cartCount = event.target;
    const count = parseInt(cartCount.textContent || "0", 10);

    if (count > 0) {
      cartCount.classList.remove("hidden");
      cartCount.classList.add("bounce");
      cartCount.addEventListener(
        "animationend",
        () => {
          cartCount.classList.remove("bounce");
        },
        { once: true }
      );

      cartCount.classList.add("highlight");
      cartCount.addEventListener(
        "animationend",
        () => {
          cartCount.classList.remove("highlight");
        },
        { once: true }
      );
    } else {
      cartCount.classList.add("hidden");
    }
  }
});
