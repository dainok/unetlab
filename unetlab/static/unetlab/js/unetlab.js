// import Alpine from "alpinejs";
import "./stores/wsStore.js";   // store WS
// import bookCrud from "./components/bookCrud.js";
import labCrud from "./components/labCrud.js";

// window.Alpine = Alpine;

// registra componenti
// Alpine.data("bookCrud", bookCrud);
// Alpine.data("labCrud", labCrud);

// Alpine.start();




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