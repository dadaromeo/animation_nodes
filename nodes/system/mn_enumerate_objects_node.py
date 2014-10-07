import bpy
from bpy.types import Node
from mn_node_base import AnimationNode
from mn_execution import nodePropertyChanged, nodeTreeChanged, allowCompiling, forbidCompiling
from mn_utils import *

class EnumerateObjectsNode(Node, AnimationNode):
	bl_idname = "EnumerateObjectsNode"
	bl_label = "Loop Objects"
	
	def getSubProgramNames(self, context):
		nodeTree = self.id_data
		subProgramNames = []
		for node in nodeTree.nodes:
			if node.bl_idname == "EnumerateObjectsStartNode": subProgramNames.append((node.subProgramName, node.subProgramName, ""))
		return subProgramNames
	def selectedProgramChanged(self, context):
		self.rebuildSubProgramSockets()
	
	subProgramsEnum = bpy.props.EnumProperty(items = getSubProgramNames, name = "Sub-Programs", update=selectedProgramChanged)
	
	def init(self, context):
		self.inputs.new("ObjectListSocket", "Objects")
		self.outputs.new("ObjectListSocket", "Objects")
		
	def draw_buttons(self, context, layout):
		layout.prop(self, "subProgramsEnum")
		rebuild = layout.operator("mn.rebuild_sub_program_sockets", "Rebuild Sockets")
		rebuild.nodeTreeName = self.id_data.name
		rebuild.nodeName = self.name
						
	def rebuildSubProgramSockets(self):
		forbidCompiling()
		connections = getConnectionDictionaries(self)
		self.removeDynamicSockets()
		startNode = self.getStartNode()
		if startNode is not None:
			for socket in startNode.sockets:
				self.inputs.new(socket.socketType, socket.socketName)
				self.outputs.new(socket.socketType, socket.socketName)
		tryToSetConnectionDictionaries(self, connections)
		allowCompiling()
		nodeTreeChanged()
		
	def removeDynamicSockets(self):
		for i, socket in enumerate(self.inputs):
			if i > 0: self.inputs.remove(socket)	
		for i, socket in enumerate(self.outputs):
			if i > 0: self.outputs.remove(socket)

	def getStartNode(self):
		subProgramName = self.subProgramsEnum
		for node in self.id_data.nodes:
			if node.bl_idname == "EnumerateObjectsStartNode":
				if node.subProgramName == subProgramName:
					return node
		return None
					

		
# register
################################
		
def register():
	bpy.utils.register_module(__name__)

def unregister():
	bpy.utils.unregister_module(__name__)