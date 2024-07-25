
#include "SimpleParameterNode.h"

#include <rclcpp/rclcpp.hpp>
#include <rcl_interfaces/msg/set_parameters_result.hpp>

#include <memory>
#include <string>
#include <vector>

SimpleParameterNode::SimpleParameterNode()
    : Node("simple_parameter")
{
    declare_parameter<int>("simple_int_param", 42);
    declare_parameter<std::string>("simple_str_param", "Don't panic!");

    param_callback_handle_ = add_on_set_parameters_callback([this](auto const& param) { return paramChangeCallback(param); });
}

rcl_interfaces::msg::SetParametersResult SimpleParameterNode::paramChangeCallback(const std::vector<rclcpp::Parameter> &parameters)
{
    rcl_interfaces::msg::SetParametersResult result;

    for (auto const& param : parameters)
    {
        if (param.get_name() == "simple_int_param" && param.get_type() == rclcpp::ParameterType::PARAMETER_INTEGER)
        {
            RCLCPP_INFO_STREAM(get_logger(), "Param simple_int_param changed! New value is: " << param.as_int());
            result.successful = true;
        }
        else
        {
            if (param.get_name() == "simple_str_param" &&
                param.get_type() == rclcpp::ParameterType::PARAMETER_STRING) {
                RCLCPP_INFO_STREAM(get_logger(), "Param simple_str_param changed! New value is: " << param.as_string());
                result.successful = true;
            }
        }
    }

    return result;
}

int main(int argc, char* argv[])
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<SimpleParameterNode>();
    rclcpp::spin(node);
    rclcpp::shutdown();

    return 0;
}
