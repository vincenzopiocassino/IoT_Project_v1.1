import { ChangeDetectorRef, Component } from '@angular/core';
import { AlertController, ModalController } from '@ionic/angular';
import { DataFire, DataService, Note, User } from '../services/data.service';
import { ModalPage } from '../modal/modal.page';

@Component({
  selector: 'app-home',
  templateUrl: 'home.page.html',
  styleUrls: ['home.page.scss'],
})
export class HomePage {
  notes: Note[] = [];
  datas: DataFire[] = [];
  user: User[] = [];



  constructor(private dataServices: DataService, private cd: ChangeDetectorRef, private alertCtrl: AlertController, private modalCtrl: ModalController) {
    this.dataServices.getNotes().subscribe(res => {
      console.log(res);
      this.notes = res;
    })
    this.dataServices.getData().subscribe(res => {
      console.log(res)
      this.datas = res;
    })
    
  }

  async addNote() {
    const alert = await this.alertCtrl.create({
      header: 'Add Note',
      inputs: [
        {
          name: 'title',
          placeholder: 'My cool note',
          type: 'text'
        },
        {
          name: 'text',
          placeholder: 'Learn Ionic',
          type: 'textarea'
        }
      ],
      buttons: [
        {
          text: 'Cancel',
          role: 'cancel'
        }, {
          text: 'Add',
          handler: res => {
            this.dataServices.addNote({ text: res.text, title: res.title })
          }
        }
      ]

    });
    await alert.present();
  }

  async openNote(note: Note) {
    const modal = await this.modalCtrl.create({
      component: ModalPage,
      componentProps: { id: note.id },
      breakpoints: [0, 0.5, 0.8],
      initialBreakpoint: 0.8
    });

    await modal.present();
  }

  async openData(datas: DataFire) {
    const modal = await this.modalCtrl.create({
      component: ModalPage,
      componentProps: { id: datas.id },
      breakpoints: [0, 0.5, 0.8],
      initialBreakpoint: 0.8
    });

    await modal.present();
  }

  async openUser(user: User , id_user: any) {
    const modal = await this.modalCtrl.create({
      component: ModalPage,
      componentProps: { id: id_user },
      breakpoints: [0, 0.5, 0.8],
      initialBreakpoint: 0.8
    });

    await modal.present();
  }
}
