# KWIP2

This project was generated with [Angular CLI](https://github.com/angular/angular-cli) version 16.1.0. To get help on the Angular CLI use `ng help` or go check out the [Angular CLI Overview and Command Reference](https://angular.io/cli) page.

## Running the application

These commands run a local version of the website on your computer for your personal use.

### Frontend

Run `ng serve` to start the frontend dev server. In your browser, go to [`http://localhost:4200/`](). The application will automatically reload if you change any of the source files.

### Backend

Run `npm run backend` to start the dev database (uses `json-server`: quick & easy dev database for testing). You can visit [http://localhost:3000/]() to view everything in the database.

Eventually we will stop using `json-server` and have a true backend in the `backend` folder.

## Development

### Linting

Linters check your code for possible mistakes and stylize your code to keep it consistent with the rest of the project.

`npm run lint-check` will tell you any warnings or errors in your code.
`npm run lint-fix` will fix any of these that it can automatically.

#### Recommended Extentions

If you're using _VSCode_, the _ESLint_ extension is recommended. It will automatically lint your code and give you warning/error squiggles in your IDE for anything that would be caught by `npm run lint-check`.

The _Prettier_ extension is also useful for keeping your code style consistent with the rest of the project. Once installed, you can turn on the "Editor: Format On Save" setting to fix things like extra newlines, using '' v.s. "", trailing commas and other things every time you save a file.

### Creating new Angular components, services, etc.

Run `ng generate component <component-name> --standalone` to generate a new component. You can also use `ng generate directive|pipe|service|class|guard|interface|enum|module`.

### Mock-ups

Mock-ups help with giving an idea for what the website should look like. Think of them as style guides. 
We have the origional mock-ups made by KMNR alumni _Elizabeth Hoffer_ and are [available here](https://drive.google.com/drive/folders/1BJ4RVYpYwLwPs1m9jhKhyHFUlajuOsvx).

## Production Tools

These are for getting the website ready to be served on the internet

### Build

Run `ng build` to build the project. The build artifacts will be stored in the `dist/` directory.

### Running unit tests

Run `ng test` to execute the unit tests via [Karma](https://karma-runner.github.io).

### Running end-to-end tests

Run `ng e2e` to execute the end-to-end tests via a platform of your choice. To use this command, you need to first add a package that implements end-to-end testing capabilities.
