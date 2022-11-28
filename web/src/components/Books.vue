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
        href="/home"
        text
      >
        <span class="mr-2">Library online</span>
      </v-btn>
    </v-app-bar>
    <v-dialog v-model="dialogBorrowList" max-width="900px">
    <v-card>
    <v-card-title
      class="ml-7"
    >
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
                <v-dialog v-model="dialogReturn" max-width="700px">
                  <v-card>
                    <v-card-title class="text-h5">Are you sure to delete this request?</v-card-title>
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
                mdi-delete-forever
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
<!--
    <v-main>
        <Books/>
    <router-view />
    </v-main>
   -->
    <v-card>
    <v-card-title
    >
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
        inset
        vertical
      ></v-divider>
        <v-dialog
          v-model="dialog"
          max-width="700px"
        >
          <template v-slot:activator="{ on, attrs }">
            <v-btn
              color="primary"
              dark
              class="ma-2"
              v-bind="attrs"
              v-on="on"
            >
              New book
            </v-btn>
          </template>
          <v-card>
            <v-card-title>
              <span class="text-h5">{{ formTitle }}</span>
            </v-card-title>

            <v-card-text>
              <v-container>
                <v-row>
                  <v-col
                    cols="12"
                    sm="6"
                    md="4"
                  >
                    <v-text-field
                      v-model="editedItem.name"
                      label="Name"
                    ></v-text-field>
                  </v-col>
                  <v-col
                    cols="12"
                    sm="6"
                    md="4"
                  >
                    <v-text-field
                      v-model="editedItem.author"
                      label="Author"
                    ></v-text-field>
                  </v-col>
                  <v-col
                    cols="12"
                    sm="6"
                    md="4"
                  >
                    <v-text-field
                      v-model="editedItem.page_count"
                      label="Page count"
                    ></v-text-field>
                  </v-col>
                  <v-col
                    cols="12"
                    sm="6"
                    md="4"
                  >
                    <v-text-field
                      v-model="editedItem.quantity"
                      label="Quantity"
                    ></v-text-field>
                  </v-col>
                  <v-col
                    class="d-flex"
                    cols="12"
                    sm="6"
                  >
                    <v-select
                      item-text="name"
                      item-value="id"
                      v-model="editedItem.category_id"
                      label="Category"
                      :items="items"
                    ></v-select>
                  </v-col>
                </v-row>
              </v-container>
            </v-card-text>

            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn
                color="blue darken-1"
                text
                @click="close"
              >
                Cancel
              </v-btn>
              <v-btn
                color="blue darken-1"
                text
                @click="save"
              >
                Save
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
        <v-dialog v-model="dialogDelete" max-width="500px">
          <v-card>
            <v-card-title class="text-h5">Are you sure you want to delete this item?</v-card-title>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="blue darken-1" text @click="closeDelete">No</v-btn>
              <v-btn color="blue darken-1" text @click="deleteItemConfirm">Yes</v-btn>
              <v-spacer></v-spacer>
            </v-card-actions>
          </v-card>
        </v-dialog>
    </template>
    <template v-slot:[`item.actions`]="{ item }">
      <v-icon
        small
        class="mr-2"
        @click="editItem(item)"
      >
        mdi-pencil
      </v-icon>
      <v-icon
        small
        @click="deleteItem(item)"
      >
        mdi-delete
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
 // import BookForm from './BookForm.vue'
 var token
 var axiosHeaders

  export default {
    name: 'book-admin',
    data: () => ({
    search: '',
    searchBorrow: '',
    menuItems: [
              { title: 'Request', icon: 'mdi-account-question', link: '' },
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
      dialog: false,
      dialogDelete: false,
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
        { text: 'Actions', value: 'actions', sortable: false },
      ],
      borrowHeaders: [
        {
          text: 'ID',
          align: ' d-none',
          sortable: false,
          value: 'id',
        },
        { text: 'ID', value: 'book_id', align: ' d-none',sortable: false},
        { text: 'Name', value: 'name', align: 'start' },
        { text: 'User', value: 'User_name'},
        { text: 'Borrow date', value: 'borrow_date' },
        { text: 'Due date', value: 'return_date' },
        { text: 'Delete request', value: 'return', sortable: false },
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
    computed: {
      formTitle () {
        return this.editedIndex === -1 ? 'New book' : 'Edit book'
      },
    },

    watch: {
      dialogBorrowList (val) {
        val || this.closeDialogBorrowList()
      },
      dialogReturn (val) {
        val || this.closeReturn()
      },
      dialog (val) {
        val || this.close()
      },
      dialogDelete (val) {
        val || this.closeDelete()
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
           // this.$emit('showInfo')
             this.datas=response.data;
            }).catch(error => {
                if (error.response.status == 403){
                    this.$toasted.show("Please log in and try again")
                    this.$router.push('/login')
                    }
                console.log(error)}
                );
      },
      borrowBook () {
        token = JSON.parse( localStorage.getItem('token') );
        axiosHeaders = {headers: {
                        'Content-Type': 'application/json',
                        "Authorization": `Bearer ${token}`
                        }};
        axios.get('http://127.0.0.1:8000/get_borrow', axiosHeaders).then((response)=>{
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
               return response;
              }).catch(error => {
                console.log(error)}
                );

        axios.patch(`http://127.0.0.1:8000/update_book/${this.borrowedItem.book_id}`, request_body, axiosHeaders)
        .then((response)=>{
              this.$toasted.show("Book returned")
              this.borrowBook();
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

      closeReturn () {
        this.dialogReturn = false
        this.searchBorrow = ''
        this.search = ''
        this.$nextTick(() => {
          this.borrowedItem = Object.assign({}, this.defaultBorrow)
          this.borrowIndex = -1
        })
      },

      editItem (item) {
        this.editedIndex = this.datas.indexOf(item)
        this.editedItem = Object.assign({}, item)
        this.dialog = true
      },

      deleteItem (item) {
        this.editedIndex = this.datas.indexOf(item)
        this.editedItem = Object.assign({}, item)
        this.dialogDelete = true
      },

      deleteItemConfirm () {
        axios.delete(`http://127.0.0.1:8000/delete_book/${this.editedItem.id}`, axiosHeaders).then((response)=>{
            this.datas.splice(this.editedIndex, 1)
            this.$toasted.show("Book deleted")
            this.closeDelete()
            return response;
        }).catch(error => {
                if (error.response.status === 403){
                    this.$toasted.show("Please log in and try again")
                    this.$router.push('/login')
                    }
                console.log(error)}
                );
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

      close () {
        this.dialog = false
        this.searchBorrow = ''
        this.search = ''
        this.$nextTick(() => {
          this.editedItem = Object.assign({}, this.defaultItem)
          this.editedIndex = -1
        })
      },

      closeDelete () {
        this.dialogDelete = false
        this.searchBorrow = ''
        this.search = ''
        this.$nextTick(() => {
          this.editedItem = Object.assign({}, this.defaultItem)
          this.editedIndex = -1
        })
      },

      save () {
        if (this.editedIndex > -1) {
            axios.patch(`http://127.0.0.1:8000/update_book/${this.editedItem.id}`, this.editedItem, axiosHeaders)
            .then((response)=>{
        //    Object.assign(this.datas[this.editedIndex], this.editedItem)
            this.$toasted.show("Book updated")
            this.initialize ();
             return response;
            }).catch(error => {
                if (error.response.status === 403){
                    this.$toasted.show("Please log in and try again")
                    this.$router.push('/login')
                    }
                console.log(error)}
                );
        } else {
             axios.post('http://127.0.0.1:8000/add_book', this.editedItem, axiosHeaders).then((response)=>{
            this.$toasted.show("Book added")
            this.initialize ();
             return response;
            }).catch(error => {
                if (error.response.status === 403){
                    this.$toasted.show("Please log in and try again")
                    this.$router.push('/login')
                    }
                console.log(error)}
                );
         //   this.datas.push(this.editedItem)
        }
        this.close()
      },
      removeToken() {
        this.$router.push('/login')
        localStorage.removeItem('token')
      }

    },
  }
</script>
<style>
</style>