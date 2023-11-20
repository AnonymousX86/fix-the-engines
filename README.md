# Fix The Engines

My very first text-based paragraph game. A story about a crewman of Epsilon IV ship who wakes up in the middle of a disaster.

## Installation

I'm using Ubuntu WSL with `pyenv`.

1. Install WSL.
   ```cmd
   wsl --install Ubuntu
   ```
   All steps are now done inside WSL.

2. Install `pyenv` - <https://github.com/pyenv/pyenv#installation>.

3. Install Python 3.11.6.
   ```sh
   pyenv install 3.11.6
   ```

4. *(Optional)* Create virtualenv.
   ```sh
   pyenv virtualenv 3.11.6 fte
   ```

5. Clone repository and `cd` into.
   ```sh
   git clone git@github.com:AnonymousX86/fix-the-engines.git
   ```

   ```sh
   cd fix-the-engines
   ```

6. Set local version.
   - With virtualenv:

     ```sh
     pyenv local fte
     ```
   - Without virtualenv:

     ```sh
     pyenv local 3.11.6
     ```

8. Install requirements (from [`requirements.txt`](/requirements.txt)).
   ```sh
   pyenv exec pip install -r requirements.txt
   ```

9. Run the game.
   ```sh
   pyenv exec python -OOm FTE
   ```

