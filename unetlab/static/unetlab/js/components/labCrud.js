import { api } from "../utils.js";

export default function labCrud() {
  return {
    form: {
      title: "Nuovo Libro",
      author_id: 1
    },

    async submit(lab_id) {
      try {
        // POST usando il tuo api helper
        const data = await api.post("/books", this.form);

        console.log("POST riuscito", data);

        // redirect alla nuova pagina
        window.location.href = `/books/${data.id}`;

      } catch (error) {
        console.error("Errore POST:", error);
        alert("Errore durante la creazione del libro");
      }
    }
  }
}
window.labCrud = labCrud;