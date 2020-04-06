import Vue from 'vue';
import Router from 'vue-router';
import Lampade from '@/components/Lampade';
import Telegram from '@/components/Telegram';
import Impostazioni from '@/components/Impostazioni';

Vue.use(Router);

export default new Router({
  routes: [
      {
        path: '/',
        redirect: '/lampade',
      },
      {
        path: '/lampade',
        name: 'Lampade',
        component: Lampade,
      },
      {
        path: '/telegram',
        name: 'Telegram',
        component: Telegram,
      },
      {
          path: '/impostazioni',
          name: 'Impostazioni',
          component: Impostazioni,
      },
  ],
});
