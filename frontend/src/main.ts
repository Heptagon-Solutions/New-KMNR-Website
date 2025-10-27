import { platformBrowserDynamic } from '@angular/platform-browser-dynamic';

import { AppModule } from './app/app.module';

// Declare MusicKit for TypeScript
declare var MusicKit: any;


platformBrowserDynamic().bootstrapModule(AppModule)
  .catch(err => console.error(err));
