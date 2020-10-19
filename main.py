#! /usr/bin/python3

import random
import copy

class Node:

	def __init__(self, data=None):
		self.data = data
		self.next = None
		self.prev = None
		self.pos = None

	def info(self):
		print("Node:")
		print("\tPosition: ", self.pos)
		print("\tData: ", self.data)
		print("\tAddress: ", self)
		print("\tPrev: ", self.prev)
		print("\tNext: ", self.next)

class LinkList:

	def __init__(self):

		self.head = None
		self.tail = None

		self.size = 0

	def isEmpty(self):
		return self.size == 0

	def getHead(self):
		return self.head

	def getTail(self):
		return self.tail

	def addHead(self, data):

		# Create a new node
		newNode = Node(data)

		# Update head and tail node
		self.head = newNode
		self.tail = newNode

		# Update size
		self.size += 1
		newNode.pos = self.size

	def addNode(self, data):

		# Add head if node is empty
		if self.isEmpty():
			self.addHead(data)
			return

		if self.size == 1:

			# Create a new node
			newNode = Node(data)

			# Update head's pointers
			self.head.next = newNode
			newNode.prev = self.head

			# Update tail node
			self.tail = newNode

			# Update size
			self.size += 1
			newNode.pos = self.size
			
			return

		# Create a new node
		newNode = Node(data)
		self.tail.next = newNode
		newNode.prev = self.tail
		self.tail = newNode

		self.size += 1
		newNode.pos = self.size

	def printForward(self):

		# Get head node
		currNode = self.getHead()
		
		while currNode != None:
			print(currNode.data)
			# print(currNode.info())
			currNode = currNode.next

	def printReverse(self):

		# Get tail node
		currNode = self.getTail()
		
		while currNode != None:
			print(currNode.data)
			# print(currNode.info())
			currNode = currNode.prev

	def printLinkListData(self):

		# Get head node
		currNode = self.getHead()

		while currNode != None:
			currNode.info()
			currNode = currNode.next

	def getMiddleNode(self, headNode):

		# OBJECTIVE: Get middle position of node from link list
		# NOTE: Cannot use self.size because a link list will be divided by half until there is only 1 left,
		# 		so the size will be changing

		# Return node if it is empty
		if headNode == None:
			return headNode

		# Set 2 positions
		slowNode = headNode
		fastNode = headNode

		# Iterate link list
		# Make sure next node and node after that exist
		while (fastNode.next != None) and (fastNode.next.next != None):

			# Update nodes
			slowNode = slowNode.next
			fastNode = fastNode.next.next

		# Return slowNode as middle node
		return slowNode

	def sortedMerge(self, linkListA, linkListB):

		# OBJECTIVE: Sort 2 halves of the same link list

		newHead = None

		# Check if either halves of the list are none
		# If data is none, then it must be a tail
		if linkListA == None or linkListA.data == None:
			return linkListB

		if linkListB == None or linkListB.data == None:
			return linkListA

		# Make a recursive call, divide called link list, and come back here
		if linkListA.data <= linkListB.data:
			newHead = linkListA
			newHead.next = self.sortedMerge(linkListA.next, linkListB)
			newHead.next.prev = newHead # Point the next node to newHead
			newHead.prev = None
		else:
			newHead = linkListB
			newHead.next = self.sortedMerge(linkListA, linkListB.next)
			newHead.next.prev = newHead # Point the next node to newHead
			newHead.prev = None

		# Return head sorted link list
		return newHead

	def mergeSort(self, headNode):

		# OBJECTIVE: Sort link list starting with head node

		# Check if link list is empty or by itself
		if (headNode == None) or (headNode.next == None):
			return headNode

		# Get middle node
		middleNode = self.getMiddleNode(headNode)
		nodeAfterMiddle = middleNode.next

		# Set pointer from middle_node to next node as None
		# NOTE: By setting next as none, middle_node would be the end of the link list
		middleNode.next = None

		# Sort left and right side of link list
		leftSide = self.mergeSort(headNode)
		rightSide = self.mergeSort(nodeAfterMiddle)

		# Merge both sides of the link list to one in sorted order.
		# The return value of sortedMerge() is the head node of the new link list
		return self.sortedMerge(leftSide, rightSide)

	def binarySearchForPosition(self, lowNode, highNode, position):

		# OBJECTIVE: Return data at specific position

		# Base cases
		if lowNode == None:
			# print("lowNode is none\n")
			return
		elif highNode == None:
			# print("highNode is none\n")
			return

		if lowNode.pos > highNode.pos:
			# print("Nodes are overlapping\n")
			return

		# Get 2 middle nodes
		middleNode = self.getMiddleNode(lowNode)
		nodeAfterMiddle = middleNode.next

		# Temporarily cut link list in half
		middleNode.next = None

		# Make a recursive call, if needed
		if middleNode.pos == position:
			# print("Node found\n")
			output = middleNode.data

		elif middleNode.pos > position:
			output = self.binarySearchForPosition(lowNode, middleNode.prev, position)

		else:
			output = self.binarySearchForPosition(nodeAfterMiddle, highNode, position)

		# Relink link list and return output
		middleNode.next = nodeAfterMiddle
		return output

	def binarySearchForNode(self, lowNode, highNode, position):

		# OBJECTIVE: Return node at specified position

		# Base cases
		if lowNode == None:
			# print("lowNode is none\n")
			return
		elif highNode == None:
			# print("highNode is none\n")
			return

		if lowNode.pos > highNode.pos:
			# print("Nodes are overlapping\n")
			return

		# Get 2 middle nodes
		middleNode = self.getMiddleNode(lowNode)
		nodeBeforeMiddle = middleNode.prev
		nodeAfterMiddle = middleNode.next

		# Temporarily cut link list in half
		middleNode.next = None

		# Make a recursive call, if needed
		if middleNode.pos > position:
			it = self.binarySearchForNode(lowNode, middleNode.prev, position)

		elif middleNode.pos < position:
			it = self.binarySearchForNode(nodeAfterMiddle, highNode, position)
		
		else:

			# Relink link list and set iterator node (it) as middleNode
			middleNode.next = nodeAfterMiddle
			it = middleNode
			return it

		# Incase in one recursive call the "else" was not met, then reconfigure link list
		middleNode.next = nodeAfterMiddle
		return it

def addRemainingNodes(newLinkList, headA):

	# OBJECTIVE: Add remaining nodes to from old link list to newLinkList

	# print("Adding remaining nodes")

	while headA != None:
		newLinkList.addNode(headA.data)
		headA = headA.next

	return newLinkList

def mergeSortA(headA, headB):
		
	# OBJECTIVE: Merge 2 sorted link list to one by calling functions from LinkList class
	# link: https://www.geeksforgeeks.org/merge-sort-for-linked-list/

	# Create a new link list
	newLinkList = LinkList()

	while True:

		# If either link list is empty, add all posents from the other link list
		if headA == None:
			newLinkList = addRemainingNodes(newLinkList, headB)
			break

		if headB == None:
			newLinkList = addRemainingNodes(newLinkList, headA)
			break

		# Compare nodes from both link list to see which goes first in sorted order
		if headA.data <= headB.data:

			# print("Adding A")

			# Update pointers
			newLinkList.addNode(headA.data)

			# Update headA
			headA = headA.next

		else:

			# print("Adding B")

			# Update pointers
			newLinkList.addNode(headB.data)

			# Update headB
			headB = headB.next

	return newLinkList

def shuffle(linkListA):

	# Create a list filled with random numbers
	randomNumbers = list()

	while len(randomNumbers) != linkListA.size:

		# Generate a random number
		r = random.randint(1, linkListA.size)

		if r not in randomNumbers:
			randomNumbers.append(r)

	# Add data in Nth position to shuffle link list
	newLinkList = LinkList()
	for pos in randomNumbers:
		data = linkListA.binarySearchForPosition(linkListA.getHead(), linkListA.getTail(), pos)
		newLinkList.addNode(data)

	# Delete list and return link list
	del randomNumbers
	return newLinkList

def iterateFromNode(currNode):

	# OBJECTIVE: Iterator link list from given node

	while currNode != None:
		print(currNode.data)
		currNode = currNode.next

if __name__ == "__main__":
	
	# Create link list
	linkListA = LinkList()
	linkListA.addNode("A")
	linkListA.addNode("B")
	linkListA.addNode("C")

	linkListB = LinkList()
	linkListB.addNode("D")
	linkListB.addNode("E")
	linkListB.addNode("F")

	# Sort link lists
	linkListC = LinkList()
	linkListC = mergeSortA(linkListA.getHead(), linkListB.getHead())

	# Shuffle a link list
	shuffleLinkList = shuffle(linkListC)

	# Get random node from link list and iterate from there
	shuffleLinkList.printForward()
	print()
	it = shuffleLinkList.binarySearchForNode(shuffleLinkList.getHead(), shuffleLinkList.getTail(), 1)
	iterateFromNode(it)