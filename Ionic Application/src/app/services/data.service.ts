import { Injectable } from '@angular/core';
import { Firestore, collection, collectionData, doc, docData, addDoc, deleteDoc, updateDoc } from '@angular/fire/firestore';
import { Observable } from 'rxjs';
import * as internal from 'stream';




export interface Note {
  id?: string;
  title: string;
  text: string;
}

export interface User {
  id?: string;
  Cognome: string;
  Nome: string;
}

export interface Device {
  id?: string;
  Modello: string;
  Targa: string;
}

export interface DataFire {
  id?: string;
  Device: string;
  Lat: string;
  Long: string;
  PhoneNumber: string;
  Reset: string;
  Status: string;
  TimeStamp: string;
  User: string;
  ModelloAuto: string;
  unix_timestamp: string;

}

@Injectable({
  providedIn: 'root'
})

export class DataService {

  constructor(private firestore: Firestore) {

  }

  getNotes(): Observable<Note[]> {
    const notesRef = collection(this.firestore, 'notes');
    return collectionData(notesRef, { idField: 'id' }) as Observable<Note[]>;
  }

  getUser(): Observable<User[]> {
    const userRef = collection(this.firestore, 'User');
    return collectionData(userRef, { idField: 'id' }) as Observable<User[]>;
  }

  getUserbyId(id: any): Observable<User> {
    const dataRef = doc(this.firestore, `User/${id}`);
    return docData(dataRef, { idField: 'id' }) as Observable<User>;
  }

  getData(): Observable<DataFire[]> {
    const dataRef = collection(this.firestore, 'Data');
    
    return collectionData(dataRef, { idField: 'id' }) as Observable<DataFire[]>;
  }

  getDatabyId(id: any): Observable<DataFire> {
    const dataRef = doc(this.firestore, `Data/${id}`);
    return docData(dataRef, { idField: 'id' }) as Observable<DataFire>;
  }

  getNotebyId(id: any): Observable<Note> {
    const noteDocRef = doc(this.firestore, `notes/${id}`);
    return docData(noteDocRef, { idField: 'id' }) as Observable<Note>;
  }

  addNote(Note: Note) {
    const notesRef = collection(this.firestore, 'notes');
    return addDoc(notesRef, Note);
  }

  deleteNote(note: Note) {
    const noteDocRef = doc(this.firestore, `notes/${note.id}`);
    return deleteDoc(noteDocRef);
  }

  updateNote(note: Note) {
    const noteDocRef = doc(this.firestore, `notes/${note.id}`);
    return updateDoc(noteDocRef, { title: note.title, text: note.text });
  }

  updateData(data: DataFire) {
    const dataRef = doc(this.firestore, `Data/${data.id}`);

    var currentdate = new Date();
    var datetime = currentdate.getDate() + "/"+ (currentdate.getMonth() + 1) + "/"+ currentdate.getFullYear() + "  " + currentdate.getHours() + ":"
      + currentdate.getMinutes() + ":"
      + currentdate.getSeconds();
    console.log(datetime);

    if (data.Status == "Preso in carico" || data.Status == "Corsa terminata") {
      alert("Il cliente è stato già preso in carico!");
      return null;
    }
    else {
      window.open("https://maps.google.com/?q=" + data.Lat + "," + data.Long);
      return updateDoc(dataRef, {
        TimeStamp: datetime, Status: "Preso in carico"
      });
    }

  }


  resetData(data: DataFire) {
    const dataRef = doc(this.firestore, `Data/${data.id}`);

    if (data.Status == "Preso in carico") {
      alert("La macchina può essere riavviata!");
      return updateDoc(dataRef, {
        Reset: "SI", Status: "Corsa terminata"
      });
    }
    else {
      alert("Il cliente non è ancora stato preso in carico!");
      return null;
    }

  }

}

