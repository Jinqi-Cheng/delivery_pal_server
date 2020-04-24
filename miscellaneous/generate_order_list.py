"""
Create Date , 
@author: 
"""
import read_pdf
import pandas as pd
import numpy as np
from Order import Order,OrderList
from sko.GA import GA_TSP
from cluster import *
def generate_list():
    order_list = OrderList()
    read_pdf.fetch_pdf("4.19 92129.pdf", order_list)
    order_list.to_csv("tmp.csv")
    # df = pd.read_csv("tmp.csv")

    df = pd.read_csv("tmp.csv", encoding='utf-8')
    df = geocode(df)
    df = analyse(df)
    # for label in set(df.label.values.tolist()):
    # print(label)
    matrix_map, ids = create_distance(df)
    print(ids)
    opt_seq = generate_sequence(matrix_map, ids)
    draw_seq(df, seq=opt_seq)
if __name__ == '__main__':
    order_list = OrderList()
    read_pdf.fetch_pdf("4.23 92129.pdf",order_list)
    order_list.to_csv("tmp.csv")
    # df = pd.read_csv("tmp.csv")

    df = pd.read_csv("tmp.csv",encoding='utf-8', index_col=False)
    # df = pd.read_csv("tmp.csv",encoding='latin1', index_col=False)
    # print(df)
    print(df.address)
    df = geocode(df)
    # df = analyse(df)
    # for label in set(df.label.values.tolist()):
        # print(label)
    matrix_map,ids = create_distance(df)
    distance_matrix = np.asarray(create_distance_matrix(df))


    def cal_total_distance(routine):
        '''The objective function. input routine, return total distance.
        cal_total_distance(np.arange(num_points))
        '''
        num_points, = routine.shape
        # print(distance_matrix)
        # print(type(distance_matrix))
        return sum([distance_matrix[routine[i % num_points], routine[(i + 1) % num_points]] for i in range(num_points)])


    # ga_tsp = GA_TSP(func=cal_total_distance, n_dim=len(distance_matrix), size_pop=50, max_iter=500, prob_mut=1)
    # best_points, best_distance = ga_tsp.run()
    # print(best_points)
    # print(ids)
    # opt_seq = generate_sequence(matrix_map,ids)
    opt_seq = first_ten_opt_seq(df)
    opt_seq = insert_point(df,opt_seq,matrix_map)
    draw_seq(df,seq=opt_seq)
    # draw_seq_index(df,best_points)
    order_list.sort(opt_seq)
    order_list.to_csv("./tmp.csv")
    # print(df)