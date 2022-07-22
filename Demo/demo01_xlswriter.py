import xlsxwriter




if __name__ == '__main__':

    book = xlsxwriter.Workbook('./demo.xlsx')
    sheet = book.add_worksheet('data')
    book.close()
