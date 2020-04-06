<template>
    <div id="app">
      <b-navbar toggleable="lg" type="dark" variant="dark">
          <b-navbar-brand href="#">Project Lamp</b-navbar-brand>
            <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

            <b-collapse id="nav-collapse" is-nav>
                <b-navbar-nav class="ml-auto">
                    <b-nav-item active-class="active" to="/lampade">Lampade</b-nav-item>
                    <b-nav-item active-class="active" to="/telegram">Telegram</b-nav-item>
                    <!--<b-nav-item active-class="active" to="/impostazioni">Impostazioni</b-nav-item>

                    <b-nav-item-dropdown right>
                        <template slot="button-content"><em>User</em></template>
                        <b-dropdown-item href="#">Profile</b-dropdown-item>
                        <b-dropdown-item href="#">Sign Out</b-dropdown-item>
                    </b-nav-item-dropdown>-->
                </b-navbar-nav>
            </b-collapse>
        </b-navbar>
    <router-view/>
  </div>
</template>

<script>
export default {
  name: 'App',
};


</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
.container {
    margin-top: 20px;
}
</style>
