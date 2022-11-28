<template>
  <div id="app">
  <v-app>
  <v-navigation-drawer
      v-model="drawer"
      app
      fixed
      temporary
    >
      <v-toolbar flat dark color="primary">
               <v-list class="title">
                    Menu
               </v-list>
            </v-toolbar>
            <v-list>
                <v-list-item
                  v-for="(item, i) in menuItems"
                  :key="i"
                  @click="openDialogBorrowList"
                >
                  <v-list-item-icon>
                    <v-icon>{{ item.icon }}</v-icon>
                  </v-list-item-icon>

                  <v-list-item-content>
                    <v-list-item-title  @click="drawer = false;">{{ item.title }}</v-list-item-title>
                  </v-list-item-content>
                </v-list-item>
              </v-list>
            <template v-slot:append>
        <div class="pa-2">
          <v-btn block @click="removeToken">
            Log out
          </v-btn>
        </div>
      </template>
    </v-navigation-drawer>
    <v-app-bar
      app
      color="primary"
      dark
    >
    <v-app-bar-nav-icon @click="drawer = !drawer"></v-app-bar-nav-icon>
      <v-btn
        href="/"
        text
      >
        <span class="mr-2">Library online</span>
      </v-btn>
    </v-app-bar>
    <v-dialog v-model="dialogBorrowList" max-width="700px">
    <v-card>
    <v-card-title>
      <span class="text-h5">Borrowed books</span>
      <v-spacer></v-spacer>

      <v-text-field
        v-model="searchBorrow"
        append-icon="mdi-magnify"
        label="Search"
        single-line
        hide-details
      ></v-text-field>
    </v-card-title>
        <v-card-text>
          <v-container>
            <v-data-table
            :headers="borrowHeaders"
            :items="borrowdatas"
            :search="searchBorrow"
            sort-by="book_id"
            class="elevation-1"
            >
            <template v-slot:top>
                <v-divider
                  class="mx-4"
                  inset
                  vertical
                ></v-divider>
                <v-spacer></v-spacer>
                <v-dialog v-model="dialogReturn" max-width="500px">
                  <v-card>
                    <v-card-title class="text-h5">Do you want to return this book?</v-card-title>
                    <v-card-actions>
                      <v-spacer></v-spacer>
                      <v-btn color="blue darken-1" text @click="closeReturn">No</v-btn>
                      <v-btn color="blue darken-1" text @click="returnItemConfirm">Yes</v-btn>
                      <v-spacer></v-spacer>
                    </v-card-actions>
                  </v-card>
                </v-dialog>
            </template>
            <template v-slot:[`item.return`]="{ item }">
              <v-icon
                small
                @click="returnItem(item)"
              >
                mdi-cart-remove
              </v-icon>
            </template>
            <template v-slot:no-data>
              <v-btn
                color="primary"
                @click="borrowBook"
              >
                Reset
              </v-btn>
            </template>
          </v-data-table>
      </v-container>
    </v-card-text>
    <v-card-actions>
      <v-spacer></v-spacer>
      <v-btn
        color="blue darken-1"
        text
        @click="closeDialogBorrowList"
      >
        Close
      </v-btn>
    </v-card-actions>
  </v-card>
  </v-dialog>
    <v-card>
    <v-card-title>
      All Books
      <v-spacer></v-spacer>
      <v-text-field
        v-model="search"
        append-icon="mdi-magnify"
        label="Search"
        single-line
        hide-details
      ></v-text-field>
    </v-card-title>
    <v-data-table
    :headers="headers"
    :items="datas"
    :search="search"
    sort-by="id"
    class="elevation-1"
  >
    <template v-slot:top>
      <v-divider
        class="mx-4"
        inset
        vertical
      ></v-divider>
        <v-dialog v-model="dialogBorrow" max-width="500px">
          <v-card>
            <v-card-title class="text-h5">Do you want to borrow this book?</v-card-title>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="blue darken-1" text @click="closeBorrow">No</v-btn>
              <v-btn color="blue darken-1" text @click="borrowItemConfirm">Yes</v-btn>
              <v-spacer></v-spacer>
            </v-card-actions>
          </v-card>
        </v-dialog>
    </template>
    <template v-slot:[`item.borrow`]="{ item }">
      <v-icon
        small
        @click="borrowItem(item)"
      >
        mdi-cart-plus
      </v-icon>
    </template>
    <template v-slot:no-data>
      <v-btn
        color="primary"
        @click="initialize"
      >
        Reset
      </v-btn>
    </template>
  </v-data-table>
  </v-card>
  </v-app>
  </div>
</template>


<script>
  import axios from 'axios'
  // import user from './user.txt'
  import jwt_Decode from "jwt-decode";
 // import BookForm from './BookForm.vue'
 var token
  var user_id
 var axiosHeaders
  export default {
    name: 'book-user',
    data: () => ({
    search: '',
    searchBorrow: '',
    menuItems: [
              { title: 'Borrowed Books', icon: 'mdi-book', link: '' },
            ],
    drawer: null,
      items:[
        {id:1, name:'Adventure stories'},
        {id:2, name:'Horror'},
        {id:3, name:'Romance'},
        {id:4, name:'Science fiction'}
      ],
      dialogReturn: false,
      dialogBorrowList: false,
      dialogBorrow: false,
      headers: [
        {
          text: 'ID',
          align: 'start',
          sortable: false,
          value: 'id',
        },
        { text: 'Category_id', value: 'category_id', align: ' d-none' },
        { text: 'Name', value: 'name' },
        { text: 'Author', value: 'author' },
        { text: 'Page count', value: 'page_count' },
        { text: 'Category', value: 'Category_name' },
        { text: 'Quantity', value: 'quantity' },
        { text: 'Borrow', value: 'borrow', sortable: false },
      ],
      borrowHeaders: [
        {
          text: 'ID',
          align: ' d-none',
          sortable: false,
          value: 'id',
        },
        { text: 'ID', value: 'book_id', align: 'start',sortable: false},
        { text: 'Name', value: 'name' },
        { text: 'Quantity', value: 'quantity', align: ' d-none'},
        { text: 'Borrow date', value: 'borrow_date' },
        { text: 'Due date', value: 'return_date' },
        { text: 'Return', value: 'return', sortable: false },
      ],
      borrowdatas: [],
      datas: [],
      editedIndex: -1,
      borrowIndex: -1,
      borrowedItem: {
        name: '',
        borrow_date: '',
        return_date: '',
        quantity: 0,
        book_id: 0,
        id: 0,
      },
      editedItem: {
        name: '',
        author: '',
        page_count: 0,
        category_id: '',
        quantity: 0,
        id: 0,
      },
      defaultItem: {
        name: '',
        author: '',
        page_count: 0,
        category_id: '',
        quantity: 0,
        id: 0,
      },
      defaultBorrow: {
        name: '',
        borrow_date: '',
        return_date: '',
        book_id: 0,
        id: 0,
      },
    }),

    watch: {
      dialogBorrowList (val) {
        val || this.closeDialogBorrowList()
      },
      dialogReturn (val) {
        val || this.closeReturn()
      },
      dialogBorrow (val) {
        val || this.closeBorrow()
      },
    },

      mounted (){
        this.initialize();
      },

    methods: {

      initialize () {
        token = JSON.parse( localStorage.getItem('token') );
        axiosHeaders = {headers: {
                        'Content-Type': 'application/json',
                        "Authorization": `Bearer ${token}`
                        }};
        axios.get('http://127.0.0.1:8000/', axiosHeaders).then((response)=>{
             this.datas=response.data;
            }).catch(error => {
                if (error.response.status === 403){
                    this.$toasted.show("Please log in and try again")
                    this.$router.push('/login')
                    }
                console.log(error)}
                );
      },
      borrowBook () {
        user_id = jwt_Decode(localStorage.getItem('token')).userid
        console.log(user_id)
        // let user_id = Number(user)
        token = JSON.parse( localStorage.getItem('token') );
        axiosHeaders = {headers: {
                        'Content-Type': 'application/json',
                        "Authorization": `Bearer ${token}`
                        }};
        axios.get(`http://127.0.0.1:8000/get_borrow/${user_id}`, axiosHeaders).then((response)=>{
             this.borrowdatas=response.data;
            }).catch(error => {
                if (error.response.status === 403){
                    this.$toasted.show("Please log in and try again")
                    this.$router.push('/login')
                    }
                console.log(error)}
                );
      },

      returnItem (item) {
        this.borrowIndex = this.borrowdatas.indexOf(item)
        this.borrowedItem = Object.assign({}, item)
        this.dialogReturn = true
      },

      returnItemConfirm () {
        this.borrowedItem.quantity += 1;
        let request_body = {
            "quantity": this.borrowedItem.quantity,
        };

        axios.delete(`http://127.0.0.1:8000/delete_borrow/${this.borrowedItem.id}`, axiosHeaders)
        .then((response)=>{
              this.borrowBook();
              this.$toasted.show("Book returned")
              return response;
              }).catch(error => {
                console.log(error)}
                );

        axios.patch(`http://127.0.0.1:8000/update_book/${this.borrowedItem.book_id}`, request_body, axiosHeaders)
        .then((response)=>{
              this.initialize ();
               return response;
              }).catch(error => {
                if (error.response.status === 403){
                    this.$toasted.show("Please log in and try again")
                    this.$router.push('/login')
                    }
                console.log(error)}
                );

        this.closeReturn()
      },

      borrowItem (item) {
        this.editedIndex = this.datas.indexOf(item)
        this.editedItem = Object.assign({}, item)
        this.dialogBorrow = true
      },

      borrowItemConfirm () {
          if (this.editedItem.quantity > 0) {
              this.editedItem.quantity -= 1;
              let request_body = {
                  "book_id": this.editedItem.id,
                  "user_id": user_id,
              };

              axios.post('http://127.0.0.1:8000/add_borrow', request_body, axiosHeaders)
              .then((response)=>{
                     return response;
                    }).catch(error => {
                      console.log(error)
                    }
                );

              axios.patch(`http://127.0.0.1:8000/update_book/${this.editedItem.id}`, this.editedItem, axiosHeaders)
              .then((response)=>{
                    this.$toasted.show("Book requested")
                    this.initialize ();
                     return response;
                    }).catch(error => {
                if (error.response.status === 403){
                    this.$toasted.show("Please log in and try again")
                    this.$router.push('/login')
                    }
                console.log(error)}
                );
              this.closeBorrow()
          }
          else {
              this.closeBorrow ()
              this.$toasted.show("Can not borrow this book")
          }
      },

      openDialogBorrowList() {
        this.borrowBook()
        this.dialogBorrowList = true
      },

      closeDialogBorrowList() {
        this.dialogBorrowList = false
        this.searchBorrow = ''
        this.search = ''
      },

      closeReturn () {
        this.dialogReturn = false
        this.searchBorrow = ''
        this.search = ''
        this.$nextTick(() => {
          this.borrowedItem = Object.assign({}, this.defaultBorrow)
          this.borrowIndex = -1
        })
      },

      closeBorrow () {
        this.dialogBorrow = false
        this.searchBorrow = ''
        this.search = ''
        this.$nextTick(() => {
          this.editedItem = Object.assign({}, this.defaultItem)
          this.editedIndex = -1
        })
      },

      removeToken() {
        this.$router.push('/login')
        token = null
        localStorage.removeItem('token')
      }
    },
  }
</script>
<style>
</style>