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
        lab__pk: pk,
      }
      await api.post("/instance/create/", payload);
    },
    async build() {
      const pk = this.$el.closest('[data-pk]').dataset.pk;
      console.log("🗑️ Build lab con pk =", pk);
    },
  };
}
