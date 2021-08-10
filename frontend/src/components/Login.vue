<template>
    <div>
        <div class="container vertical-center">
            <div class="card w-50 mx-auto">
                <div class="card-body m-2">
                    <div class="form-group text-left">
                        <label for="login">Nome de usuário</label>
                        <input type="text" class="form-control" id="login" v-model="login">
                    </div>
                    <div class="form-group text-left">
                        <label for="password">Senha</label>
                        <input type="password" class="form-control" id="password" v-model="password">
                        <small v-if="error" class="text-danger"> Autenticação falhou. </small>
                    </div>
                    <b-button class="btn btn-info btn-block" @click="doLogin">Entrar</b-button>
                </div>
            </div>
        </div>
    </div>
    
</template>

<script>
import axios from 'axios'

export default {
    name: 'login',
    data() {
        return {
            login: null,
            password: null,
            error: false,
        }
    },
    beforeCreate() {
        if (this.$session.exists()) this.$router.push('/folders');
    },
    methods: {
        doLogin() {
            this.error = false;
            axios.post(this.backend + '/login', {
                'login' : this.login,
                'password' : this.password,
            }).then(res => {
                if (res.status === 200) {
                    this.$session.start();
                    this.$session.set('user_id', res.data.user_id);
                    this.$session.set('user_name', res.data.name);
                    this.$session.set('user_privileged', res.data.privileged);
                    this.$router.push('/folders');
                } else {
                    this.error = true;
                }
            }).catch(err => {
                this.error = true;
                console.log(err);
            });
        },
    }
}
</script>

<style scoped>
.vertical-center {
    min-height: 80%;
    min-height: 80vh;
    display: flex;
    align-items: center;
}
</style>
