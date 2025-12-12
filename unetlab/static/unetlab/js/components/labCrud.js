import { api } from "../utils.js";

export function labCrud() {
  return {
    async create() {
      const pk = this.$el.closest('[data-pk]').dataset.pk;
      console.log("✅ Creo lab con pk =", pk);
    },
    async read() {
      const pk = this.$el.closest('[data-pk]').dataset.pk;
      console.log("🗑️ Leggo lab con pk =", pk);
    },
    async update() {
      const pk = this.$el.closest('[data-pk]').dataset.pk;
      console.log("✅ Aggiorno lab con pk =", pk);
    },
    async remove() {
      const pk = this.$el.closest('[data-pk]').dataset.pk;
      console.log("🗑️ Cancello lab con pk =", pk);
    },
    async start() {
      const pk = this.$el.closest('[data-pk]').dataset.pk;
      const payload = {
        lab_id: parseInt(pk, 10),
      }
      const response = await api.post("/instance/", payload);
      window.location.href = `/instance/${response.data.id}/`;
    },
    async build() {
      const pk = this.$el.closest('[data-pk]').dataset.pk;
      console.log("🗑️ Build lab con pk =", pk);
    },
  };
}
