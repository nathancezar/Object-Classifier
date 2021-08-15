<template>
    <div>
        <menuHeader :controlButtons="true"> </menuHeader>
        <div class="container">
            <template v-if="!loaded">
                <div class="d-flex justify-content-center my-5">
                    <b-spinner label="Loading..."></b-spinner>
                </div>
            </template>
            <div v-show="loaded">
                <b-table
                    :items="filtered"
                    bordered
                    :fields="fields"
                    class="center"
                    head-variant="dark"
                    :sort-compare="userPrivileged ? sortCompare : null"
                    sort-by="status"
                    striped>

                    <template slot="top-row" slot-scope="{ fields }">
                        <td v-for="field in fields" :key="field.key">
                            <b-form-input
                                class="m-0"
                                size="sm"
                                v-if="fieldIsFiltered(field)"
                                v-model="filters[field.key]"
                                :placeholder="field.label">
                            </b-form-input>
                        </td>
                    </template>

                    <template v-slot:cell(name)="data">
                        <template v-if="userPrivileged">
                            <b-link :id="data.value" @click="verify(data.item)">
                                {{ data.value }}
                            </b-link>
                            <b-tooltip :target="data.value" title="Verificar pasta"></b-tooltip>                            
                         </template>
                         <template v-else>
                             {{ data.value }}
                         </template>
                    </template>

                    <template v-slot:cell(user)="data">
                        {{ data.value }}
                    </template>

                    <!-- <template v-slot:cell(processed_count)="data">
                        {{ data.value ? data.value : 0 }} de {{data.item.total_count}}
                    </template> -->

                    <template v-slot:cell(status)="data">
                        {{ data.value }}
                    </template>

                    <template v-slot:cell(action)="data">
                        <template v-if="data.item.deleted">
                            <b-button
                                v-if="userPrivileged"
                                class="btn btn-warning"
                                size="sm"
                                @click="restoreFolder(data.item)">
                                Restaurar
                            </b-button>
                        </template>
                        <template v-else>
                            <b-button
                                v-if="!data.item.processed && (!data.item.user_id || data.item.user_id === userId) && !data.item.flagged"
                                class="btn btn-info"
                                size="sm"
                                @click="validateClassify(data.item, data.item.user_id)">
                                Classificar
                            </b-button>
                            <b-button
                                v-else-if="data.item.processed && userPrivileged"
                                class="btn btn-warning"
                                size="sm"
                                @click="showExportModal(data.item)">
                                <b-icon-arrow-bar-down> </b-icon-arrow-bar-down>
                            </b-button>
                            <b-button
                                v-if="userPrivileged"
                                class="btn btn-warning m-1"
                                size="sm"
                                @click="showDeleteModal(data.item)">
                                <b-icon-x> </b-icon-x>
                            </b-button>
                        </template>
                        
                    </template>

                    <template v-slot:head(exported)="data">
                        <span id="exportedLabel"> {{ data.label }} </span>
                        <b-tooltip target="exportedLabel" title="Exportado"></b-tooltip>
                    </template>

                    <template v-slot:head(verified)="data">
                        <span id="verifiedLabel"> {{ data.label }} </span>
                        <b-tooltip target="verifiedLabel" title="Verificado"></b-tooltip>
                    </template>

                    <template v-slot:cell(exported)="data">
                        <b-form-checkbox v-model="data.value" disabled style="padding-left:32px;"> </b-form-checkbox>
                    </template>

                    <template v-slot:cell(verified)="data">
                        <b-form-checkbox v-model="data.value" disabled style="padding-left:32px;"> </b-form-checkbox>
                    </template>
                </b-table>
            </div>
        </div>
        <b-modal
            id="export-modal"
            ok-title="Exportar"
            ok-variant="warning"
            cancel-title="Cancelar"
            @ok="exportLabels">
            <template v-slot:modal-title>
                <span v-if="exportFolder"> Exportar labels da pasta {{ exportFolder.name }} </span>
                <span v-else> Exportar labels </span>
            </template>
            <b-form-group label="Escolha o formato:">
                <b-form-radio v-model="exportFormat" value="yolo"> YOLO </b-form-radio>
                <b-form-radio v-model="exportFormat" value="faster"> Faster R-CNN </b-form-radio>
            </b-form-group>
        </b-modal>
        <b-modal
            id="delete-modal"
            ok-title="Excluir"
            ok-variant="warning"
            cancel-title="Cancelar"
            @ok="deleteFolder">
            <template v-slot:modal-title>
                Excluir pasta
            </template>
            <p>
                Tem certeza que deseja excluir a pasta <b>{{ folderToDelete.name }}</b>?
            </p>
        </b-modal>
    </div>
</template>
<script>
import axios from 'axios'
import { BIconArrowBarDown, BIconX } from 'bootstrap-vue';
import menuHeader from './shared/Header.vue'


export default {
    name: 'folders',
    components: {
        menuHeader,
        BIconArrowBarDown,
        BIconX,
    },
    data() {
        return {
            fields: [],
            fieldsUnprivileged: [
                { 'key' : 'name', 'label' : 'Nome', 'sortable' : true },
                { 'key' : 'user', 'label' : 'Usuário', 'sortable' : true },
                // { 'key' : 'processed_count', 'label' : 'Imagens' },
                { 'key' : 'status', 'label' : 'Status', 'sortable' : true},
                { 'key' : 'action', 'label' : 'Ações'},
            ],
            fieldsPrivileged: [
                { 'key' : 'exported', 'label' : 'E', 'sortable' : true },
                { 'key' : 'verified', 'label' : 'V', 'sortable' : true },
            ],
            filters: {
                'name': '',
                'user': '',
                'status': '',
            },
            folders: [],
            loaded: false,
            userId: null,
            userPrivileged: null,
            exportFolder: {
                name: '',
            },
            exportFormat: 'yolo',
            folderToDelete: {
                id: null,
                name: '',
            },
        }
    },
    computed: {
        filtered() {
            if (this.folders.length > 0) {
                const filtered = this.folders.filter(item => {
                    return Object.keys(this.filters).every(key => 
                        String(item[key]).includes(this.filters[key]))
                })
                return filtered.length > 0 ? filtered : [];
            }
            return [];
        },
    },
    beforeCreate() {
        if (!this.$session.exists()) this.$router.push('/login');
    },
    mounted() {
        this.$root.$on('export-all',  this.showExportModal);
    },
    created() {
        this.refresh();
    },
    methods: {
        refresh() {
            this.loaded = false;
            this.userId = this.$session.get('user_id');
            this.userPrivileged = this.$session.get('user_privileged');
            this.fields = this.fieldsUnprivileged;
            if (this.userPrivileged) {
                this.fields = this.fields.concat(this.fieldsPrivileged);
            }
            this.folders = [];
            axios.get(this.backend + '/folders').then((res) => {
                if (res.data) {
                    res.data.folders.forEach((el) => {
                        el.status = el.processed ? 
                            "Processado" : (el.user_id ? "Em processamento" : "Disponível");
                        if (el.flagged) el._rowVariant = 'warning';
                        if (el.deleted) el._rowVariant = 'danger';
                        if (this.userPrivileged || (!el.flagged && !el.deleted))
                            this.folders.push(el);
                    });
                }
                this.loaded = true;
            }).catch(err => console.log(err));
        },
        validateClassify(folder) {
            axios.put(this.backend + '/folders/user_id', {
                'folder_id': folder.id,
                'user_id': this.$session.get('user_id'),
            }).then(res => {
                console.log(res);
                if (res.data.response) {
                    this.classify(folder);
                } else {
                    this.refresh();
                }
            }).catch(err => console.log(err));
        },
        verify(folder) {
            this.$router.push({
                name: 'classify',
                params: {
                    'folder': folder,
                    'verifying': 1,
                }
            });
        },
        classify(folder) {
            this.$router.push({
                name: 'classify',
                params: {
                    'folder': folder,
                    'verifying': 0,
                }
            });
        },
        showExportModal(folder) {
            this.exportFolder = folder;
            this.$bvModal.show('export-modal');
        },
        exportLabels() {
            if (this.exportFolder) {
                axios.put(this.backend + '/folders/export_folder', {
                    'folder_id': this.exportFolder.id,
                    'format': this.exportFormat,
                }).then(res => {
                    if (res.status === 200) {
                        const index = this.folders.findIndex(item => item.id === res.data.id);
                        this.folders[index].exported = true;
                        this.$bvToast.toast(`Pasta ${res.data.name} exportada.`, {
                            title: 'Sucesso!',
                            variant: 'success',
                            autoHideDelay: 5000,
                            appendToast: true,
                        });
                    }
                }).catch(err => {
                    this.$bvToast.toast(`Não foi possível exportar a pasta. ${err}.`, {
                        title: 'Erro durante exportação',
                        variant: 'danger',
                        noAutoHide: true,
                        appendToast: true,
                    });
                });
            } else {
                axios.put(this.backend + '/folders/export_all', {
                    'format': this.exportFormat,
                }).then(res => {
                    if (res.status === 200) this.refresh();
                }).catch(err => {
                    this.$bvToast.toast(`Erro ao exportar pastas. ${err}.`, {
                        title: 'Erro durante exportação',
                        variant: 'danger',
                        noAutoHide: true,
                        appendToast: true,
                    });
                });
            }
        },
        fieldIsFiltered(field) {
            return Object.keys(this.filters).includes(field.key);
        },
        sortCompare(aRow, bRow, _, sortDesc) {
            //(..., key, sortDesc, formatter, compareOptions, compareLocale
            if (aRow.deleted && !bRow.deleted) return sortDesc ? -1 : 1;
            if (bRow.deleted && !aRow.deleted) return sortDesc ? 1 : -1;
            if (aRow.flagged && !bRow.flagged) return sortDesc ? 1 : -1;
            if (bRow.flagged && !aRow.flagged) return sortDesc ? -1 : 1;
            return null;
        },
        showDeleteModal(folder) {
            this.folderToDelete = folder;
            this.$bvModal.show('delete-modal');
        },
        deleteFolder() {
            axios.put(this.backend + "/folders/deleted", {
                folder_id: this.folderToDelete.id,
                deleted: true,
            }).then(res => {
                if (res.status === 200) {
                    const index = this.folders.findIndex(item => item.id === res.data.folder_id);
                    this.folders[index].deleted = true;
                    this.folders[index]._rowVariant = 'danger';
                    this.$bvToast.toast(`Pasta excluída.`, {
                        title: 'Sucesso!',
                        variant: 'success',
                        autoHideDelay: 5000,
                        appendToast: true,
                    });
                }
            }).catch(err => {
                this.$bvToast.toast(`Erro ao excluir pasta. ${err}.`, {
                    title: 'Erro durante exclusão',
                    variant: 'danger',
                    noAutoHide: true,
                    appendToast: true,
                });
            });
        },
        restoreFolder(folder) {
            axios.put(this.backend + "/folders/deleted", {
                folder_id: folder.id,
                deleted: false,
            }).then(res => {
                if (res.status === 200) {
                    const index = this.folders.findIndex(item => item.id === res.data.folder_id);
                    this.folders[index].deleted = false;
                    this.folders[index]._rowVariant = '';
                    this.$bvToast.toast(`Pasta ${folder.name} restaurada.`, {
                        title: 'Sucesso!',
                        variant: 'success',
                        autoHideDelay: 5000,
                        appendToast: true,
                    });
                }
            }).catch(err => {
                this.$bvToast.toast(`Erro ao restaurar pasta ${folder.name}. ${err}.`, {
                    title: 'Erro durante restauração',
                    variant: 'danger',
                    noAutoHide: true,
                    appendToast: true,
                });
            });
        },
    }
}
</script>

<style scoped>

.center {
    text-align: center;
}

</style>
