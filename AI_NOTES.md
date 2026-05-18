### 1. Which parts did Claude write end-to-end?

Claude helped create most of the project structure, including the Flask backend (server.py), database schema, seed script with 100 food items, and the frontend HTML/CSS/JS. It also helped build the swipe gesture logic, card animations, and results page. The file structure and technology choices were discussed and decided together.

### 2. Where did I push back or fix Claude’s output?

One example was the backend setup. Claude first suggested using Node.js/Express with better-sqlite3, but the package had compile issues because it required node-gyp and native binaries. I decided to switch to Python/Flask with the built-in sqlite3 module because it was simpler and worked better in the environment.

I also reviewed the undo feature. Claude’s first version removed the vote from the server during undo. I simplified it to a client-side-only undo because adding full server-side undo support would require more API endpoints and extra error handling, which was outside the project timeline.

### 3. One thing Claude did better than expected

Claude generated 100 unique food items with good descriptions and cuisine categories very quickly. This saved a lot of time, and the overall quality was better than expected.

### 4. One thing Claude did worse than expected

The mobile swipe gesture implementation needed multiple fixes. The first version did not properly handle touch-action: none, so page scrolling interfered with horizontal swiping on mobile devices. I had to guide Claude to focus more on mobile-first behavior and iPhone screen size testing.

### 5. What other AI tools were used?

No other AI tools were used for this project. Claude was the only AI assistant used for coding, debugging, and design decisions.
