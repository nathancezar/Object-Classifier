import Vue from 'vue';
import Router from 'vue-router';
import VueSession from 'vue-session';

Vue.use(Router);
Vue.use(VueSession, { persist: true });


export default new Router({
  routes: [
    {
      path: '/login',
      name: 'login',
      component: require('@/components/Login').default,
    },
    {
      path: '/folders',
      name: 'folders',
      component: require('@/components/Folders').default,
    },
    {
      path: '/classify',
      name: 'classify',
      component: require('@/components/Classifier').default,
      props: true,
    },
    {
      path: '*',
      redirect: '/login',
    },
  ],
});
