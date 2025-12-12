import { labCrud } from "./components/labCrud.js";
import { registerWsStore } from "./stores/wsStore.js";

// Register websocket store
registerWsStore();

// Wait for Alpine and register components
document.addEventListener("alpine:init", () => {
  Alpine.data("labCrud", labCrud);
});


// project/
// │── index.html          # entrypoint principale
// │
// │── js/                 # tutto il codice Alpine
// │    ├── main.js        # inizializzazione Alpine
// │    ├── utils.js       # funzioni comuni (fetch, validazioni)
// │    ├── stores/        # Alpine.store() per stato condiviso
// │    │    ├── booksStore.js
// │    │    ├── authorsStore.js
// │    │    └── collectionsStore.js
// │    └── components/    # Alpine.data() o funzioni x-data
// │         ├── crud.js
// │         ├── modal.js
// │         └── form.js
// │
// └── css/
//      └── style.css      # eventuali stili globali (se non usi Tailwind)
