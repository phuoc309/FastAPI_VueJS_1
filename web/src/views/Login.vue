<template>
   <v-app id="inspire">
      <v-main>
         <v-container fluid fill-height>
            <v-layout align-center justify-center>
               <v-flex xs12 sm8 md4>
                  <v-card class="elevation-12">
                     <v-toolbar dark color="primary">
                        <v-toolbar-title>Log in</v-toolbar-title>
                     </v-toolbar>
                     <v-form>
                     <v-card-text>
                           <v-text-field
                               autofocus
                              prepend-icon="mdi-account"
                              v-model="account.name"
                              name="user"
                              label="User"
                              type="text"
                               @keyup.enter="login()"
                           ></v-text-field>
                           <v-text-field
                              id="password"
                              prepend-icon="mdi-lock"
                              v-model="account.password"
                              name="password"
                              label="Password"
                              type="password"
                               @keyup.enter="login()"
                           ></v-text-field>
                     </v-card-text>
                     <v-card-actions>
                        <v-spacer></v-spacer>
                        <v-btn color="primary" @click=login()>Log in</v-btn>
                     </v-card-actions>
                    </v-form>
                  </v-card>
               </v-flex>
            </v-layout>
         </v-container>
      </v-main>
   </v-app>
</template>

<script>
import axios from 'axios'
export default {
   name: 'LoginForm',
   data: () => ({
       account: {
            name: '',
            password: '',
          },
  }),

   methods: {

      login () {
        axios.post('http://127.0.0.1:8000/login',
        {
            "name": this.account.name,
            "password": this.account.password
        }, {headers: {
        'Content-Type': 'application/json'}}).then((response)=>{
            if(response.status == 200){
            localStorage.setItem( 'token', JSON.stringify(response.data.token) )
                console.log(typeof (response.data.token));
                if(this.account.name == 'admin') {
                    this.$router.push('/home')
                }
                else {
                    this.$router.push('/')
                }
            }
        }).catch(error => {this.$toasted.show("User or password is incorrect"), console.log(error)});
      },
   }
};
</script>

<style></style>
