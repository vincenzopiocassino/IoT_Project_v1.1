import { Component, Input, OnInit } from '@angular/core';
import { DataFire,Note, DataService } from '../services/data.service';
import { ModalController, ToastController } from '@ionic/angular';
import { Data } from '@angular/router';


@Component({
  selector: 'app-modal',
  templateUrl: './modal.page.html',
  styleUrls: ['./modal.page.scss'],
})

export class ModalPage implements OnInit {
  @Input() id?: string;
  data: DataFire = null as any;
  note: Note = null as any;

  constructor(private dataServices: DataService, private modalCtrl: ModalController, private toastCtrl: ToastController) { }

  ngOnInit() {
    this.dataServices.getDatabyId(this.id).subscribe(res => {
      this.data = res;
    });
  }

  async deleteNote() {
    await this.dataServices.deleteNote(this.note)
    this.modalCtrl.dismiss();
  }

  async updateNote() {
    await this.dataServices.updateNote(this.note);
    const toast = await this.toastCtrl.create({
      message: 'Note updated!.',
      duration: 2000
    });
    toast.present();

  }


  async updateData() {
    await this.dataServices.updateData(this.data);

  }

  async resetData() {
    await this.dataServices.resetData(this.data);

  }
}