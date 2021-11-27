import json
import argparse

parser = argparse.ArgumentParser(
    description='list all the nodes jumping into a given node reference')

parser.add_argument(
    'file',
    metavar='F',
    type=str,
    help='a string containing the corpus location')

parser.add_argument(
    'target',
    metavar='N',
    type=str,
    help='a string containing the node that you want to check all the jumps')

args = parser.parse_args()


_nodes_dict = {}

def prepare_dict(file_location):
    # reading the corpus data
    try:
        with open(file_location, encoding='utf-8') as json_file:
            data_json = json.load(json_file)
        # for each node in the corpus
        for node in data_json['dialog_nodes']:
            node_name = node['dialog_node']
            # add node to dict if it's not already there
            if node_name not in _nodes_dict:
                _nodes_dict.update({node_name: []})
            try:
                next_step = node['next_step']
                # if the current node jumps to another node
                if next_step and next_step['behavior'] == 'jump_to':
                    target_node = next_step['dialog_node']
                    # add jump target to dict if it's not already there
                    if target_node not in _nodes_dict:
                        _nodes_dict.update({target_node: []})
                    # updates the dict appending the current node into the target node list
                    _nodes_dict[target_node].append(node_name)
            except:
                pass
    except Exception:
        print(Exception)


def track_jump(file_location, tracked_node):
    print(tracked_node)
    prepare_dict(file_location=file_location)
    try:
        if tracked_node not in _nodes_dict:
            print(f'{tracked_node} is not a valid node')
            return

        jumps = _nodes_dict[tracked_node]

        if len(jumps) < 1:
            print(f'no jumps found goint into the {tracked_node} node')
            return
        
        print(f'{len(jumps)} node(s) found jumping into node {tracked_node}:\n')
        print(*(x for x in jumps), sep='\n')

    except Exception:
        print(Exception)


def __main__():
    track_jump(args.file, args.target)


if __name__ == "__main__":
    __main__()