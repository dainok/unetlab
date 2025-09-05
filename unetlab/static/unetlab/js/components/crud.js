import { api } from "../utils.js";

export default function crud(resource) {
    return {
        items: [],
        form: {},
        async fetchAll() {
            this.items = await api.get(`/${resource}`);
        },
        async save() {
            if (this.form.id) {
                await api.put(`/${resource}/${this.form.id}`, this.form);
            } else {
                await api.post(`/${resource}`, this.form);
            }
            this.fetchAll();
            this.reset();
        },
        edit(item) {
            this.form = { ...item };
        },
        async remove(id) {
            if (confirm("Sei sicuro?")) {
                await api.delete(`/${resource}/${id}`);
                this.fetchAll();
            }
        },
        reset() {
            this.form = {};
        }
    }
}
