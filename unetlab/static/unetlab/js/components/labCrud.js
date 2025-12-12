import { api } from '../utils.js';

export function labCrud() {
    return {
        async create() {
            console.log('➕ Create a new lab');
        },
        async read() {
            const pk = this.$el.closest('[data-pk]').dataset.pk;
            console.log('📖 Read lab with pk =', pk);
        },
        async update() {
            const pk = this.$el.closest('[data-pk]').dataset.pk;
            console.log('📝 Update lab with pk =', pk);
        },
        async delete() {
            const pk = this.$el.closest('[data-pk]').dataset.pk;
            console.log('🗑️ Delete lab with pk =', pk);
        },
        async start() {
            const pk = this.$el.closest('[data-pk]').dataset.pk;
            console.log('▶️ Start lab with pk =', pk);
            const payload = {
                lab_id: parseInt(pk, 10),
            }
            const response = await api.post('/instance/', payload);
            if (response.status >= 200 && response.status < 300) {
                window.location.href = '/instance/${response.data.id}/';
            }
        },
        async build() {
            const pk = this.$el.closest('[data-pk]').dataset.pk;
            console.log('⚒️ Build lab with pk =', pk);
            const response = await api.post('/lab/${pk}/build');
            if (response.status >= 200 && response.status < 300) {
                window.location.reload();
            }
        },
    };
}
