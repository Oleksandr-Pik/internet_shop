document.addEventListener("DOMContentLoaded", () => {
  // --- Відправка форми на сервер ---
  async function sendCartForm(form, actionBtn = null) {
    if (!form) return;

    const formData = new FormData(form);

    if (actionBtn && actionBtn.name === "action") {
      formData.set("action", actionBtn.value);
    }

    try {
      const res = await fetch(form.getAttribute("action"), {
        method: "POST",
        body: formData,
        headers: { "X-Requested-With": "XMLHttpRequest" },
      });

      const contentType = res.headers.get("content-type") || "";
      if (!contentType.includes("application/json")) {
        const text = await res.text();
        throw new Error("Non-JSON response: " + text.slice(0, 200));
      }

      const data = await res.json();

      // --- Оновлюємо лічильник кошика у шапці ---
      const counter = document.getElementById("cart-count");
      if (counter && data.cart_count !== undefined) {
        counter.textContent = data.cart_count;
      }
      

      // --- Оновлюємо кошик на сторінці ---
      if (data.product_id) {
        const row = document.getElementById(`cart-row-${data.product_id}`);
        if (row) {
          if (data.quantity === 0) {
            row.remove();
          } else {
            const qtyEl = row.querySelector(".quantity");
            if (qtyEl) qtyEl.textContent = data.quantity;

            const rowTotalEl = row.querySelector("td:nth-child(5)");
            if (rowTotalEl) rowTotalEl.textContent = data.row_total + " грн";
          }
        }

        const totalEl = document.getElementById("cart-total");
        if (totalEl) {
          const p = totalEl.querySelector("p");
          if (p)
            p.innerHTML = `<strong>Загальна сума:</strong> ${data.cart_total} грн`;
        }
      }
    } catch (err) {
      console.error("Cart action error:", err);
    }
  }

  // --- Всі форми кошика (+/-/видалити) ---
  const cartForms = document.querySelectorAll(".quantity-form, .remove-form");
  cartForms.forEach((form) => {
    form.addEventListener("submit", (e) => {
      e.preventDefault();
      const btn =
        e.submitter || e.target.querySelector('button[type="submit"]');
      sendCartForm(form, btn);
    });
  });

  // --- Додати в кошик на сторінці продукту ---
  const addForms = document.querySelectorAll(".add-to-cart-form");
  addForms.forEach((form) => {
    form.addEventListener("submit", (e) => {
      e.preventDefault();
      sendCartForm(form);
    });
  });
});
