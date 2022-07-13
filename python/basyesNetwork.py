import numpy as np
from typing import Union
from rich import print
from rich.console import Console
from rich.table import Column, Table
from collections import OrderedDict


class Node(object):
    def __init__(self,name : str,domain : Union[list,set],table : dict):
        self.name = name
        self.domain= domain
        self.table = table
    def __str__(self):
        return f"{self.name} -> {self.domain}"
    def __repr__(self):
        return f"Network Node({self.name})"
    def __hash__(self):
        return hash(self.name)
    def __eq__(self,other):
        return self.name == other.name
    def query_probability(self,name):
        if name not in self.table:
            raise ValueError(f"{name} not in this node's domain")
        return self.table[name]       

class Edge(object):
    def __init__(self,start : Node,end : Node):
        """
        start --> end
        """
        self.s = start
        self.e   = end
    def start(self):
        return self.s
    def end(self):
        return self.e

class ProbTable(object):
    def __init__(self,nodes,result):
        self.nodes = nodes
        self.result = result
    def add_probability(self,probability_rows : dict):
        self.probability_rows = probability_rows
    def get_names(self):
        return [n.name for n in self.nodes]
    def query_probability(self,row):
        for k,v in self.probability_rows.items():
            if set(k) == set(row):
                return v
        return 1.0
    def print_table(self):
        console = Console()
        table = Table(show_header=True, header_style="bold magenta")
        for n in self.nodes:
            table.add_column(n.name, style="dim", width=12)
        table.add_column(f"reason({self.result.name})", style="dim",width=12)
        for k,v in self.probability_rows.items():
            k = list(map(str,k))
            k.append(str(v))
            table.add_row(*k)
        console.print(table)



class BayesianNetwork(object):
    def __init__(self,nodes,edges):
        self.edges = edges
        self.nodes = nodes
        self.hastable = {n : False for n in self.nodes}
        self.tables   = dict()
    def add_table(self,table):
        self.tables[table.result.name] = table

    def query_unfilled_table(self):
        console = Console()
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("result", style="dim", width=12)
        table.add_column("reason", style="dim",width=12)
        for node in self.nodes:
            if self.hastable[node] == True:continue
            parents = self.get_parents(node)
            if len(parents) >= 1 :
                table.add_row(f"{node.name}",
                              f"{','.join(map(lambda x : x.name, parents))}")
        console.print(table)
    
    
    def get_parents(self,node : Node):
        return [edge.start() for edge in self.edges if edge.end() == node]
    
    def add_tables(self,tables):
        for t in tables:
            self.add_table(t)

    def _find_value(self,variables,values,n):
        for node,v in zip(variables,values):
            if node.name == n:
                return v
    def interface(self,parameters : dict):
        pass


if __name__ == "__main__":
    ## example

    server1 = Node("Server1",{"T","F"},{"T" : 0.4,"F" : 0.6})
    server2 = Node("Server2",{"T","F"},{"T" : 0.3,"F" : 0.7})
    user    = Node("User",{"T","F"},{"T" : 0.3,"F" : 0.7})
    network = BayesianNetwork([server1,server2,user],
                              [Edge(server1,server2),
                               Edge(server1,user),
                               Edge(server2,user)])
    table1 = ProbTable([server1],server2)
    table1.add_probability(
                        {
                            ("F","T") : 0.3,
                            ("F","F") : 0.7,
                            ("T","T") : 0.7,
                            ("T","F") : 0.3
                         })
    table2 = ProbTable([server2,server1],user)
    table2.add_probability({
                ("F","F","T") : 0,
                ("F","F","F") : 1,
                ("F","T","T") : 1,
                ("F","T","F") : 0,
                ("T","F","T") : 1,
                ("T","F","F") : 0,
                ("T","T","T") : 1,
                ("T","T","F") : 0,
            })
    table1.print_table()
    table2.print_table()
    network.add_tables([table1,table2])
    print(network.tables)
    print(network.interfaces({server1 : "T",server2 : "F",user : "T"}))