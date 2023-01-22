import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
    name: 'sortByTimestamp'
})
export class SortByTimestampPipe implements PipeTransform {

    transform(value: any[], args?: any): any {
        if (!value || value.length === 0 || !args) {
            return value;
        }
        let sortColumnName = args;
        if (value[0][sortColumnName] && typeof value[0][sortColumnName] === 'string') {
            value.sort((a, b) => {
                if (Number(a[sortColumnName]) < Number(b[sortColumnName])) {
                    return 1;
                } else if (Number(a[sortColumnName]) > Number(b[sortColumnName])) {
                    return -1;
                } else {
                    return 0;
                }
            });
        } else {
            value.sort((a, b) => {
                if (a[sortColumnName] < b[sortColumnName]) {
                    return 1;
                } else if (a[sortColumnName] > b[sortColumnName]) {
                    return -1;
                } else {
                    return 0;
                }
            });
        }
        return value;
    }
}
