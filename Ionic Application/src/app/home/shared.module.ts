import { NgModule } from '@angular/core';
import { SortByTimestampPipe } from './sortByTimestamp.pipe';

@NgModule({
    declarations: [SortByTimestampPipe],
    exports: [SortByTimestampPipe]
})
export class SharedModule { }
