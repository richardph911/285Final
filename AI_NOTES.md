### 1. Which parts did Claude write end-to-end?

Claude helped create most of the project structure, including the Flask backend (server.py), database schema using SQLite, seed script with 100 food items, and the frontend HTML/CSS/JS. It also helped build the swipe gesture logic, card animations, and results page.

### 2. Where did I push back or fix Claude’s output?

One example was the backend setup. Claude first suggested using Node.js/Express with better-sqlite3, but the package had compile issues because it required node-gyp and native binaries. I decided to switch to Python/Flask with the built-in sqlite3 module because it was simpler and worked better in the environment and we learn Python in class and homework so it is easier to implement.

I also reviewed the undo feature. Claude’s first version removed the vote from the server during undo. I simplified it to a client-side-only undo because adding full server-side undo support would require more API endpoints and extra error handling, which was outside the project timeline.

### 3. One thing Claude did better than expected

Claude generated 100 unique food items with good descriptions, image collections so I dont have to collect 100 images and cuisine categories very quickly. This saved a lot of time.

### 4. One thing Claude did worse than expected

So far I dont think it is worst, I think Claude did everything good. No complains in this situation. However, the color could have be better and I did fix with font and color theme.

### 5. What other AI tools were used?

No other AI tools were used for this project. Claude was the only AI assistant used for coding, debugging, and design decisions.
