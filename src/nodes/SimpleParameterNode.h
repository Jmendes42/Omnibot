
#ifndef OMNIBOT_SIMPLE_PARAMETER_NODE_H
#define OMNIBOT_SIMPLE_PARAMETER_NODE_H

#include <rclcpp/node.hpp>

class SimpleParameterNode : public rclcpp::Node
{
public:
    SimpleParameterNode();

private:
    rcl_interfaces::msg::SetParametersResult paramChangeCallback(std::vector<rclcpp::Parameter> const& parameters);

    OnSetParametersCallbackHandle::SharedPtr _setParametersCallbackHandle;
};


#endif
